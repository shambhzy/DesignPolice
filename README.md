# DesignPolice

## Installation Steps

### 1. Create a Virtual Environment

```sh
python -m venv venv
```

### 2. Activate the Virtual Environment

#### On macOS/Linux:

```sh
source venv/bin/activate
```

#### On Windows:

```sh
venv\Scripts\activate
```

### 3. Install Dependencies

```sh
pip install -r requirements.txt
```

## Running the FastAPI Server

### 1. Start the Server with Uvicorn

```sh
uvicorn main:app --reload
```

- `main` refers to the filename `main.py`
- `app` is the FastAPI instance inside `main.py`
- `--reload` enables auto-reloading for development

### 2. Access the API


- Swagger UI for API documentation: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- Use the swagger doc for making api calls directly

## Example `main.py`

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}
```

## Deactivating the Virtual Environment

```sh
deactivate
```

