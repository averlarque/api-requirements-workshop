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
    title='09.11.23 Webinar API Examples - Practical case',
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
          description='''**Experience API** for HR app allowing to add a new [Employee](https://www.merriam-webster.com/dictionary/employee) in a simplified way. Create a new Employee record associated with a specific Employer. Employee uniqueness is checked by a combination of firstName, lastName, dateOfBirth, taxId.\n 
          System API: POST /v1/employees''')
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
         response_model=EmployeeSearchResult,
         tags=[tags['system']],
         summary='Search Employee with GET' )
async def searchEmployees(firstName: str | None = None,
                        lastName: str | None = None,
                        status: str | None = None,
                        businessId: str | None = None,
                        department: str | None = None,
                        addedSince: date | None = None,
                        employerId: UUID| None = None,
                        offset: int = Query(0, title="Offset", ge=0), 
                        limit: int = Query(10, le=100, title="Limit"),
                        sort_by: str = Query("lastName", description="Sort items by field"),
                        order: str = Query("asc", description="Sort order (asc or desc)")):
    with open('examples/employees.json', 'r') as file:
        json_data = file.read()
    parsed_data = json.loads(json_data)

    result = []

    if any((firstName, lastName, status, businessId, department, addedSince, employerId)):
        for item_data in parsed_data:
            item = Employee(**item_data)

            # Apply filtering logic based on query parameters
            if ((not firstName or firstName == item.firstName) and
                (not lastName or lastName == item.lastName) and
                (not status or status == item.status) and
                (not businessId or businessId == item.businessId) and
                (not department or department == item.employmentInfo.department) and
                (not addedSince or (item.employmentInfo.startDate is not None and addedSince <= item.employmentInfo.startDate)) and
                (not employerId or employerId == item.employmentInfo.employerRef)):
                result.append(item)
    else:
        # No query parameters provided, return the full list
        for item_data in parsed_data:
            item = Employee(**item_data)
            result.append(item)    
        
    return EmployeeSearchResult(result=result, pagination=Pagination(offset=offset, limit=limit))

# Details API
@app.get("/v1/employees/{employeeId}",
         tags=[tags['system']],
         response_model=Employee,
         summary='Retrieve Employee Details')
async def getEmployeeDetails(employeeId: UUID) -> Employee:
    with open('examples/employees.json', 'r') as file:
        json_data = file.read()
    parsed_data = json.loads(json_data)
    result = None
    for item in parsed_data:
        # print(item)
        item = Employee(**item)
        if employeeId == item.id:
            result = item
            print(item.id)
            break
    else:
        raise HTTPException(status_code=404, detail='Employer is not found')
    return result

# Search policies
@app.post("/v1/policies",
        tags=[tags['system']],
        response_model=PolicySearchResult,
        summary='Searh Policies')
async def searchPolicies(body: PolicySearch,
                        offset: int = Query(0, title="Offset", ge=0), 
                        limit: int = Query(10, le=100, title="Limit")):
    pass

# Search claims
@app.post("/v1/claims",
        tags=[tags['system']],
        response_model=ClaimSearchResult,
        summary='Searh Claims')
async def searchPolicies(body: ClaimSearch,
                        offset: int = Query(0, title="Offset", ge=0), 
                        limit: int = Query(10, le=100, title="Limit")):
    pass