# TechIntellect - Simplified Employee Management System

A simple FastAPI application for employee data management with Elasticsearch backend.

## Project Structure

```
techintellect/
├── app.py                    # Main FastAPI application
├── app.conf                  # Simple configuration
├── module_register.json      # Module registration
├── run.py                    # Development server
├── requirements.txt          # Dependencies
├── static/                   # Frontend files
│   └── index.html
├── pdfs/                     # Generated PDF reports
└── src/                      # Source code
    └── employee/             # Employee module
        ├── controllers.py    # API endpoints
        └── services.py       # Business logic
```

## Quick Start

1. **Start Elasticsearch** (using Docker):
   ```bash
   docker-compose up -d elasticsearch
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python run.py
   ```

4. **Access the app**:
   - Frontend: http://localhost:8000
   - API: http://localhost:8000/api/v1/

## API Endpoints

- `POST /api/v1/upload-data` - Upload employee data
- `GET /api/v1/generate-pdf` - Generate PDF report
- `GET /api/v1/es-status` - Check Elasticsearch connection
- `GET /api/v1/health` - Health check
- `GET /` - Frontend interface

## Configuration

Edit `app.conf` to change settings:
```
ELASTICSEARCH_HOST=http://localhost:9200
INDEX_NAME=employee_data
```

## Usage

1. Open http://localhost:8000 in your browser
2. Fill out the employee form
3. Click "Upload Data" to save to Elasticsearch
4. Click "Generate PDF" to create reports
