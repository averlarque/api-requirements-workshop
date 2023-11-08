from pydantic import BaseModel, Field
from enums import *
from uuid import UUID
from datetime import date, datetime
from typing import List

current_date = datetime.now().date()

class CreateEmploymentInfo(BaseModel):
    employmentType: EmploymentType
    division: str = Field(None, description='Organization Division', example='R&D')
    position: str = Field(None, description='Employee Position', example='Scrum Master')
    effectiveDate: date = Field(..., description='Start Work Date', example=current_date)

class CreateEmployee(BaseModel):
    firstName: str = Field(..., description='First Name', example='Jay')
    lastName: str = Field(..., description='Last Name', example='Goldberg')
    middleName: str = Field(None, description='Middle Name', example= "")
    dateOfBirth: date = Field(..., description='Date of Birth', example='1990-01-01')
    taxId: str = Field(..., description='Social Security Number', example='1234-5678-2345-3456')
    employmentInfo: List[CreateEmploymentInfo]

class CreateEmployeeSuccess(BaseModel):
    employeeId: UUID = Field(..., description="Employee UID")

class EmploymentInfo(BaseModel):
    employmentType: EmploymentType
    department: str = Field(None, description='Organization Department', example='R&D')
    position: str = Field(None, description='Employee Position', example='Scrum Master')
    employerRef: UUID
    startDate: date = Field(..., description='Employment Start Date', example=current_date)
    endDate: date | None = Field(None, description='Employment End Date')

class Address(BaseModel):
    id: UUID = Field(..., description='Address UID')
    addressLine1: str = Field(..., description='Address Line 1', example=
                              '22 Acacia Avenue')
    addressLine2: str | None = Field(None, description='Address Line 2')
    city: str = Field(..., description="City Name", example='Salt Lake City')
    postalCode: str = Field(..., description="ZIP/Postal Code", example='84130')
    stateCd: str = Field(
        None, example='UT', description='US States abbreviation')
    countryCd: str = Field("US", description="ISO Country code")
    type: List[AddressContactType]

class Contact(BaseModel):
    email: str = Field(..., description="Email", example= "name@domain.com")
    phone: str = Field(..., description="Phone Number", example='+1-233-435-656')
    id: UUID = Field(..., description="Contcact UID")
    type: List[AddressContactType]

class EmployeePolicyInfo(BaseModel):
    policyRef: UUID
    premiumAmount: str = Field(..., description="Premium Payment Amount", example="50.00")
    premiumAmountCurrencyCode: str = Field(..., description="Currency ISO Code", example="USD")
    premiumPaymentFrequency: str = Field(..., description="Payment Frequency", example="BI-WEEKLY")
    startDate: date = Field(..., description="Policy Effective Date")

class Employee(BaseModel):
    id: UUID = Field(..., description='Employee UID')
    businessId: str = Field(..., description='Employee Registry Number', example='EE1023394')
    firstName: str = Field(..., description='First Name', example='John')
    lastName: str = Field(..., description='Last Name', example='Doe')
    middleName: str = Field(None, description='Middle Name', example= "")
    dob: date = Field(..., description='Date of Birth', example='1990-01-01')
    ssn: str = Field(..., description='Social Security Number', example='1234-5678-2345-3456')
    addedDate: date = Field(..., description='When Added', example=current_date)
    state: EntityStatus
    employmentInfo: List[EmploymentInfo]
    addresses: List[Address] | None = None
    contactInfo: Contact | None = None
    policies: List[EmployeePolicyInfo] | None = None

class EmployeeCreateUpdate(Employee):
    id: UUID | None = None
    businessId: str | None = None
    
class Policy(BaseModel):
    id: UUID = Field(..., description="Policy UID")
    businessId: str = Field(..., description="Policy Business ID", example="P109109")
    policyType: PolicyType
    limitAmount: float = Field(..., description="Policy Limit Payment Amount", example=10000.00)
    limitAmountCurrencyCd: str = "USD"
    status: EntityStatus
    effectiveDate: date

class DateQuery(BaseModel):
    frm: date | datetime | None = None
    to: date | datetime | None = None
    matches: List[date] | List[datetime] | None

class PolicySearch(BaseModel):
    id: List[UUID] | None = None
    businessId: List[str] | None = None
    policyType: List[PolicyType] | None = None
    status: List[EntityStatus] | None = None
    effectiveDate: DateQuery | None = None

class ClaimSearch(BaseModel):
    id: List[UUID] | None = None
    businessId: List[str] | None = None
    claimantRef: List[UUID] | None = None
    status: List[EntityStatus] | None = None
    effectiveDate: DateQuery | None = None
    policyRef: List[UUID] | None = None

class Claim(BaseModel):
    id: UUID = Field(..., description="Claim UID")
    businessId: str = Field(..., description="Claim Business ID", example="C109109")
    claimantRef: UUID
    status: EntityStatus
    policyRef: UUID
    reason: str
    lossAmount: float = Field(..., description="Claim Loss Amount", example=500.00)
    lossAmountCurrencyCd: str = "USD"
    status: EntityStatus
    effectiveDate: date

class Pagination(BaseModel):
    offset: int
    limit: int

class EmployeeSearchResult(BaseModel):
    result: List[Employee]
    pagination: Pagination

class ClaimSearchResult(BaseModel):
    result: List[Claim]
    pagination: Pagination

class PolicySearchResult(BaseModel):
    result: List[Policy]
    pagination: Pagination