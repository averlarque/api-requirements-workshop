from enum import Enum

class EmploymentType (str, Enum):
    partTime = 'PART-TIME'
    fullTime = 'FULL-TIME'

class EntityStatus(str, Enum):
    active = 'ACTIVE'
    disabled = 'DISABLED'
    pending = 'PENDING'

class AddressContactType(str, Enum):
    legal = 'LEGAL'
    work = 'WORK'
    personal = 'PERSONAL'
    billing = 'BILLING'
    mailing = 'MAILING'

class PolicyType(str, Enum):
    accidental = 'ACCIDENTAL HEALTH'
    hospital = 'HOSPITAL INDEMNITY'
    life = 'LIFE'