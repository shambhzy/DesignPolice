from fastapi import FastAPI, BackgroundTasks, HTTPException, Depends
from pydantic import BaseModel
from datetime import datetime
import logging
import uuid, asyncio
from typing import List, Optional
from config import get_settings
from services.github_service import GitHubAdapter
from services.gemini_service import GeminiAdapter
from detectors import SmellDetectorFactory
from refactoring import RefactoringStrategy
from config import Settings
from utils.file_handler import FileHandler

# Models
class ScanResponse(BaseModel):
    scan_id: str
    message: str
    started_at: datetime

class IssueDetail(BaseModel):
    file_path: str
    issue_type: str
    description: str
    suggested_fix: str

class ScanStatus(BaseModel):
    scan_id: str
    status: str
    issues: Optional[List[IssueDetail]] = None
    completed_at: Optional[datetime] = None

# App initialization
app = FastAPI(title="Code Smell Detector", version="1.0.0")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
scan_results = {}

async def run_analysis(scan_id: str, settings: Settings):
    try:
        logger.info(f"Starting analysis for scan {scan_id}")
        
        # Initialize services
        github_service = GitHubAdapter(settings)
        gemini_service = GeminiAdapter(settings.gemini_api_key)
        detector_factory = SmellDetectorFactory(gemini_service)
        
        # Get all repository files
        files = await github_service.get_repository_files("")

        issues: List[IssueDetail] = []
        
        # Process each file
        for file_info in files:
            # Skip if file is not supported or is a directory
            if file_info.get("type") == "dir" or not FileHandler.is_supported_file(
                file_info["name"], 
                settings.supported_extensions
            ):
                continue
                
            try:
                # Get file content
                file_content = await github_service.get_file_content(file_info["path"])
                
                # Skip if file is too large
                if FileHandler.get_file_size(file_content) > settings.max_file_size:
                    logger.warning(f"File {file_info['path']} exceeds size limit, skipping")
                    continue
                
                # Run all detectors in parallel
                detector_tasks = []
                for smell_type in ["large_class", "duplicate_code"]:
                    detector = detector_factory.get_detector(smell_type)
                    if detector:
                        detector_tasks.append(
                            detector.detect(file_content, file_info["path"])
                        )
                
                # Gather results from all detectors
                detector_results = await asyncio.gather(*detector_tasks, return_exceptions=True)
                
                # Process detector results
                for result in detector_results:
                    if isinstance(result, Exception):
                        logger.error(f"Detector error: {str(result)}")
                        continue
                    
                    if result:  # If issues were found
                        # Create issue details
                        file_issues = [
                            IssueDetail(
                                file_path=file_info["path"],
                                issue_type=issue.get("type", "unknown"),
                                description=issue.get("description", ""),
                                suggested_fix=issue.get("suggested_fix", "")
                            )
                            for issue in result
                        ]
                        issues.extend(file_issues)
                        
                        # Attempt refactoring for each issue
                        for issue in file_issues:
                            try:
                                strategy = RefactoringStrategy(gemini_service).get_strategy(issue.issue_type)
                                if strategy:
                                    refactored_code = await strategy.refactor(
                                        {"description": issue.description}, 
                                        file_content
                                    )
                                    
                                    if refactored_code:
                                        # Create branch name based on issue type and file
                                        branch_name = f"refactor-{issue.issue_type}-{scan_id}"
                                        
                                        # Create pull request
                                        await github_service.create_pull_request(
                                            branch_name=branch_name,
                                            file_path=issue.file_path,
                                            new_code=refactored_code,
                                            title=f"Refactor: Fix {issue.issue_type} in {issue.file_path}",
                                            description=f"""
                                            Automated refactoring to address code smell:
                                            
                                            Issue: {issue.description}
                                            
                                            Suggested Fix: {issue.suggested_fix}
                                            """
                                        )
                            except Exception as e:
                                logger.error(f"Error during refactoring: {str(e)}")
                                continue
                
            except Exception as file_error:
                logger.error(f"Error processing file {file_info['path']}: {str(file_error)}")
                continue
        
        # Update scan status with results
        scan_results[scan_id] = ScanStatus(
            scan_id=scan_id,
            status="completed",
            issues=issues,
            completed_at=datetime.now()
        )
        
        logger.info(f"Analysis completed for scan {scan_id}. Found {len(issues)} issues.")
        
    except Exception as e:
        logger.error(f"Error in analysis: {str(e)}")
        scan_results[scan_id] = ScanStatus(
            scan_id=scan_id,
            status="failed",
            completed_at=datetime.now()
        )

@app.post("/scan", response_model=ScanResponse)
async def scan_repository(background_tasks: BackgroundTasks, settings: Settings = Depends(get_settings)):
    scan_id = str(uuid.uuid4())
    scan_results[scan_id] = ScanStatus(scan_id=scan_id, status="in_progress")
    background_tasks.add_task(run_analysis, scan_id, settings)
    return ScanResponse(
        scan_id=scan_id,
        message="Scanning started",
        started_at=datetime.now()
    )

@app.get("/scan/{scan_id}", response_model=ScanStatus)
async def get_scan(scan_id: str):
    if scan_id not in scan_results:
        raise HTTPException(status_code=404, detail="Scan not found")
    return scan_results[scan_id]
