from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from ..services.services import EmployeeService

router = APIRouter()

employee_service = EmployeeService()

@router.post("/upload-data")
async def upload_employee_data(data: Dict[Any, Any]):
    result = employee_service.upload_data(data)

    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    return {
        "message": result["message"],
        "document_id": result["document_id"],
        "status": result["status"]
    }

@router.get("/generate-pdf")
async def generate_employee_pdf():
    result = employee_service.generate_pdf()

    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    return {
        "message": result["message"],
        "filename": result["filename"],
        "download_url": result["download_url"],
        "status": result["status"]
    }

@router.get("/es-status")
async def get_elasticsearch_status():
    result = employee_service.check_es_status()

    return result

@router.put("/update-employee")
async def update_employee_data(data: Dict[Any, Any]):
    result = employee_service.update_employee(data)

    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    return result

@router.delete("/delete-employee")
async def delete_employee_data(data: Dict[Any, Any]):
    result = employee_service.delete_employee(data)

    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    return result

@router.get("/employee/{emp_id}")
async def get_employee_by_id(emp_id: str):
    """Get employee data by ID."""
    result = employee_service.get_employee(emp_id)

    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])

    return result

@router.get("/employees")
async def list_employees():
    """Get list of all employees."""
    result = employee_service.list_employees()

    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    return result

@router.get("/health")
async def health_check():
    return {
        "module": "employee",
        "status": "OK",
        "service": "TechIntellect Employee API"
    }
