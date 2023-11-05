from fastapi import FastAPI, Path, Query, HTTPException
from schemas import *
from uuid import uuid4, UUID
from typing import Annotated
from enums import EntityStatus
import json

tags = {
    "experience": "Experience API",
    "system": "System API"
}

app = FastAPI(
    title='09.11.23 Webinar API Examples',
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
          summary='Create a new Employee with minimal attributes')
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

# System API

# Create/Update API
@app.post("/v1/employees",
          tags=[tags['system']],
          summary='Create/Update Employee')
async def createUpdateEmployee(body: EmployeeCreateUpdate) -> Employee:
    return body

# GET Search API
@app.get("/v1/employees",
         response_model=list[Employee],
         tags=[tags['system']],
         summary='Search Employee via GET' )
async def searchEmployees(firstName: str | None = None,
                        lastName: str | None = None,
                        status: str | None = None,
                        businessId: str | None = None,
                        department: str | None = None,
                        addedSince: date | None = None,
                        employerId: UUID| None = None,
                        offset: int = Query(0, title="Offset", ge=0), 
                        limit: int = Query(10, le=100, title="Limit")):
    with open('examples/employees.json', 'r') as file:
        json_data = file.read()
    parsed_data = json.loads(json_data)

    result = []
    for item in parsed_data:
        # print(item)
        item = Employee(**item)

        # function to add item if it is unique
        # query search item
        if firstName is not None and firstName == item.firstName:
            if item not in result: result.append(item)
        if lastName is not None and lastName == item.lastName:
            if item not in result: result.append(item)
        if status is not None and status == item.status:
            if item not in result: result.append(item)
        if businessId == item.businessId:
            if item not in result: result.append(item)
        if department == item.employmentInfo.department:
            if item not in result: result.append(item)
        if (item.employmentInfo.startDate is not None and 
            addedSince is not None and 
            addedSince <= item.employmentInfo.startDate):
            if item not in result: result.append(item)
        if employerId == item.employmentInfo.employerRef:
            if item not in result: result.append(item)
        
    return result

# Details API
@app.get("v1/employees/{employeeId}",
         tags=[tags['system']],
         response_model=Employee)
async def getEmployeeDetails(employeeId) -> Employee:
    pass