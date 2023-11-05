from pydantic import BaseModel, Field
from enums import *
from uuid import UUID
from datetime import date, datetime
from typing import List

current_date = datetime.now().date()

class CreateEmploymentInfo(BaseModel):
    employmentType: EmploymentType
    division: str = Field(None, description='Organization division', example='R&D')
    position: str = Field(None, description='Employee position', example='Scrum Master')
    effectiveDate: date = Field(..., description='Start work date', example=current_date)

class CreateEmployee(BaseModel):
    firstName: str = Field(..., description='First Name', example='Jay')
    lastName: str = Field(..., description='Last Name', example='Goldberg')
    middleName: str = Field(None, description='Middle Name', example= "")
    dateOfBirth: date = Field(..., description='Date of Birth', example='1990-01-01')
    taxId: str = Field(..., description='Social Security Number', example='1234-5678-2345-3456')
    employmentInfo: CreateEmploymentInfo

class CreateEmployeeSuccess(BaseModel):
    employeeId: UUID = Field(..., title="Employee UID")

class EmploymentInfo(BaseModel):
    employmentType: EmploymentType
    department: str = Field(None, description='Organization department', example='R&D')
    position: str = Field(None, description='Employee position', example='Scrum Master')
    employerRef: UUID
    startDate: date = Field(..., description='Employment start date', example=current_date)
    endDate: date | None = Field(None, description='Employment end date', example="")

class Address(BaseModel):
    id: UUID = Field(..., title='Address ID', examples=[
                     '913ec1e3-4952-31a6-a24d-9ff71794ae40'])
    addressLine1: str = Field(..., title='Address Line 1', examples=[
                              '22 Acacia Avenue'])
    addressLine2: str | None = Field(None, title='Address Line 1')
    city: str = Field(..., examples=['Salt Lake City'])
    postalCode: str = Field(..., examples=['84130'])
    stateCd: str = Field(
        None, examples=['UT'], description='US States abbreviation')
    countryCd: str = Field("US", description="ISO Country code")
    type: List[AddressContactType]

class Contact(BaseModel):
    email: str
    phone: str
    id: str
    type: List[AddressContactType]

class EmployeePolicyInfo(BaseModel):
    policyRef: UUID
    premiumAmount: str
    premiumAmountCurrencyCode: str
    premiumPaymentFrequency: str
    startDate: date

class Employee(BaseModel):
    id: UUID = Field(..., description='Employee UID')
    businessId: str = Field(..., description='Employee Registry Number', example='EE1023394')
    firstName: str = Field(..., description='First Name', example='John')
    lastName: str = Field(..., description='Last Name', example='Doe')
    middleName: str = Field(None, description='Middle Name', example= "")
    dob: date = Field(..., description='Date of Birth', example='1990-01-01')
    taxId: str = Field(..., description='Social Security Number', example='1234-5678-2345-3456')
    addedDate: date = Field(..., description='When Added', example=current_date)
    status: EntityStatus
    employmentInfo: EmploymentInfo
    addresses: List[Address] | None = None
    contactInfo: Contact | None = None
    policies: List[EmployeePolicyInfo] | None = None

class EmployeeCreateUpdate(Employee):
    id: UUID | None = None
    businessId: str | None = None
    
class Policy(BaseModel):
    id: UUID
    policyType: PolicyType
    limitAmount: float
    limitAmountCurrencyCd: str = "USD"
    status: EntityStatus
    effectiveDate: date

class Claim(BaseModel):
    id: UUID
    claimantRef: UUID
    status: EntityStatus
    policyRef: UUID
    reason: str
    lossAmount: float
    lossAmountCurrencyCd: str = "USD"
    status: EntityStatus
    effectiveDate: date