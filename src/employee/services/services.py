from elasticsearch import Elasticsearch
from fpdf import FPDF
from typing import Dict, Any, List
import os
from datetime import datetime

class EmployeeService:

    def __init__(self):
        self.es = Elasticsearch("http://localhost:9200")

    def upload_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            if not self.es.ping():
                return {"error": "Elasticsearch not available"}

            required_fields = ["Emp_ID"]
            for field in required_fields:
                if field not in data:
                    return {"error": f"Missing required field: {field}"}

            doc_id = str(data["Emp_ID"])
            result = self.es.index(index="employee_data", id=doc_id, document=data)

            return {
                "message": "Data uploaded successfully",
                "document_id": result["_id"],
                "status": "success"
            }
        except Exception as e:
            return {"error": f"Failed to upload data: {str(e)}"}

    def generate_pdf(self) -> Dict[str, Any]:
        try:
            if not self.es.ping():
                return {"error": "Elasticsearch not available"}

            result = self.es.search(index="employee_data", body={"query": {"match_all": {}}})
            employees = result["hits"]["hits"]

            if not employees:
                return {"error": "No employee data found"}

            # Validate first employee has required fields
            first_employee = employees[0]["_source"]
            required_fields = ["Emp_ID"]
            for field in required_fields:
                if field not in first_employee:
                    return {"error": f"Missing required field: {field}"}

            pdf_filename = f"employees_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            pdf_path = os.path.join("pdfs", pdf_filename)

            pdf = FPDF()
            pdf.set_auto_page_break(auto=True, margin=15)

            pdf.add_page()
            pdf.set_font("Arial", size=20, style='B')
            pdf.cell(200, 20, txt="Employees", ln=True, align='C')
            pdf.set_font("Arial", size=14)
            pdf.cell(200, 10, txt=f"Total Employees: {len(employees)}", ln=True, align='C')

            for i, emp_hit in enumerate(employees, 1):
                emp_data = emp_hit["_source"]

                pdf.add_page()

                pdf.set_font("Arial", size=16)
                pdf.cell(190, 12, txt=f"Employee {i}: {emp_data.get('Emp_Name', 'N/A')}", ln=True)
                pdf.ln(5)

                pdf.set_font("Arial", size=12)

                details = [
                    ("Employee ID", str(emp_data.get("Emp_ID", "N/A"))),
                    ("Name", emp_data.get("Emp_Name", "N/A")),
                    ("Designation", emp_data.get("Designation", "N/A")),
                    ("Age", str(emp_data.get("Age", "N/A"))),
                    ("Account Number", emp_data.get("Account", "N/A")),
                    ("IFSC Code", emp_data.get("IFSC", "N/A")),
                    ("Gross Pay", "Rs. " + str(emp_data.get('Gross_pay', 0))),
                    ("Net Pay", "Rs. " + str(emp_data.get('Net_pay', 0))),
                    ("Basic Pay", "Rs. " + str(emp_data.get('Basic_pay', 0))),
                    ("DA", "Rs. " + str(emp_data.get('DA', 0))),
                    ("HRA", "Rs. " + str(emp_data.get('HRA', 0))),
                    ("Grade Pay", "Rs. " + str(emp_data.get('Grade_pay', 0))),
                    ("Educational Allowance", "Rs. " + str(emp_data.get('Educational_allowance', 0))),
                    ("Conveyance Allowance", "Rs. " + str(emp_data.get('Conveyance_allowance', 0))),
                    ("Marriage Allowance", "Rs. " + str(emp_data.get('Marriage_Allowance', 0))),
                    ("Incentive", "Rs. " + str(emp_data.get('Incentive', 0))),
                    ("Arrear", "Rs. " + str(emp_data.get('Arrear', 0))),
                    ("PF", "Rs. " + str(emp_data.get('PF', 0))),
                    ("ESI", "Rs. " + str(emp_data.get('ESI', 0))),
                    ("TDS", "Rs. " + str(emp_data.get('TDS', 0))),
                    ("Professional Tax", "Rs. " + str(emp_data.get('Professional_Tax', 0))),
                    ("Advance Recovery", "Rs. " + str(emp_data.get('Advance_recovery', 0))),
                    ("SQ Rent", "Rs. " + str(emp_data.get('SQ_rent', 0))),
                    ("Food", "Rs. " + str(emp_data.get('Food', 0))),
                    ("Transport", "Rs. " + str(emp_data.get('Transport', 0))),
                    ("Mobile", "Rs. " + str(emp_data.get('Mobile', 0))),
                    ("Staff Club Fund", "Rs. " + str(emp_data.get('Staff_club_fund', 0))),
                    ("Caution Deposit", "Rs. " + str(emp_data.get('Caution_deposit', 0))),
                    ("Insurance", "Rs. " + str(emp_data.get('Insurance', 0))),
                    ("Net Pay", "Rs. " + str(emp_data.get('Net_pay', 0))),
                    ("Total Pay", "Rs. " + str(emp_data.get('Gross_pay', 0) + emp_data.get('Net_pay', 0))),
                ]

                for label, value in details:
                    pdf.cell(50, 8, txt=f"{label}:", border=0)
                    pdf.cell(0, 8, txt=str(value), ln=True)
                    pdf.ln(3)

                pdf.ln(5)

            pdf.output(pdf_path)

            return {
                "message": "PDF generated successfully",
                "filename": pdf_filename,
                "download_url": f"/pdfs/{pdf_filename}",
                "status": "success"
            }

        except Exception as e:
            return {"error": f"Failed to generate PDF: {str(e)}"}


    def check_es_status(self) -> Dict[str, Any]:
        try:
            connected = self.es.ping()
            return {
                "elasticsearch": "connected" if connected else "disconnected",
                "status": "OK" if connected else "ERROR"
            }
        except Exception as e:
            return {"elasticsearch": "error", "status": "ERROR", "message": str(e)}
