from pydantic import BaseModel, Field
from enums import *
from uuid import UUID
from datetime import date, datetime
from typing import List

current_date = datetime.now().date()

class CreateEmploymentInfo(BaseModel):
    employmentType: EmploymentType
    division: str = Field(None, title='Organization division', example='R&D')
    position: str = Field(None, title='Employee position', example='Scrum Master')
    effectiveDate: date = Field(..., title='Start work date', example=current_date)

class CreateEmployee(BaseModel):
    firstName: str = Field(..., title='First Name', example='Jay')
    lastName: str = Field(..., title='Last Name', example='Goldberg')
    middleName: str = Field(None, title='Middle Name', example= "")
    dateOfBirth: date = Field(..., title='Date of Birth', example='1990-01-01')
    taxId: str = Field(..., title='Social Security Number', example='1234-5678-2345-3456')
    employmentInfo: CreateEmploymentInfo

class CreateEmployeeSuccess(BaseModel):
    employeeId: UUID = Field(..., title="Employee UID")

class EmploymentInfo(BaseModel):
    employmentType: EmploymentType
    department: str
    position: str
    employerRef: UUID
    startDate: date
    endDate: date | None = None

class Address(BaseModel):
    id: UUID = Field(..., title='Address ID', examples=[
                     '913ec1e3-4952-31a6-a24d-9ff71794ae40'])
    addressLine1: str = Field(..., title='Address Line 1', examples=[
                              '22 Acacia Avenue'])
    addressLine2: str = Field(None, title='Address Line 1')
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
    id: UUID
    businessId: str
    firstName: str
    lastName: str
    middleName: str | None = None
    dob: date
    taxId: str
    addedDate: datetime
    status: EntityStatus
    employmentInfo: EmploymentInfo
    addresses: List[Address]
    contactInfo: Contact
    
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