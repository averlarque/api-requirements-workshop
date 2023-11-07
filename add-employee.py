from fastapi import FastAPI, Path, Query, HTTPException
from schemas import CreateEmployee, CreateEmployeeSuccess
from uuid import uuid4, UUID
from typing import Annotated
from enums import EntityStatus
import json

tags = {
    "experience": "Experience API",
    "system": "System API"
}

app = FastAPI(
    title='09.11.23 Webinar API Examples - Add Employee',
    version = '1.0.0',
    description="API implementation examples for 2nd part of IIBA Belarus Chapter webinar 'Requirements & API'",
    contact={
        "name": "Ilya Zakharau",
        "url" : 'https://ilyazakharau.com/',
        'email': 'ilya.zakharau@gmail.com'
    },
    license={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    }
)
random_uuid = str(uuid4())
# Experience API

@app.post("/v1/employer/{employerId}/employee/create",
          tags=[tags['experience']],
          summary='Create a new Employee with minimal attributes',
          description='**Experience API** for HR app allowing to add a new [Employee](https://www.merriam-webster.com/dictionary/employee) in a simplified way.')
async def createEmployee(employerId: Annotated[str, Path(title='Employer UID', example=random_uuid )],
                         body: CreateEmployee, 
                         status: EntityStatus = EntityStatus.active) -> CreateEmployeeSuccess:
    # logic for validating employerId
    if len(employerId) > 256:
        raise HTTPException(status_code=420, detail="Wrong format of Employer UID" )
    if employerId != random_uuid:
        raise HTTPException(status_code=404, detail='Employer is not found')
    # random response value
    response_value = str(uuid4())
    return CreateEmployeeSuccess(employeeId=response_value)