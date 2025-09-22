# TechIntellect FastAPI

Simple FastAPI application with health endpoint and Elasticsearch integration.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python run.py
```

3. Test the endpoints:
```bash
# Health check
curl http://localhost:8000/health

# Elasticsearch status
curl http://localhost:8000/es-status

# Upload sample data from data.json (curl method)
curl -X POST http://localhost:8000/upload-data \
  -H "Content-Type: application/json" \
  -d @data.json
```

Expected responses:
- Health: `{"status": "OK"}`
- ES Status: `{"elasticsearch": "connected", "status": "OK"}` (if ES is running)
- Upload: Success message with document ID

## API Endpoints

- `GET /` - Welcome message
- `GET /health` - Application health check
- `GET /es-status` - Elasticsearch connection status
- `POST /upload-data` - Upload employee data with validation

## Dependencies

- **FastAPI**: Web framework
- **Uvicorn**: ASGI server
- **Elasticsearch**: Search and analytics engine client
- **Requests**: HTTP library for the upload script
