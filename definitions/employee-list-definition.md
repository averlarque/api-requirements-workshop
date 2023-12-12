# Practical case for Employee Search API for HR

First you need to find internal APIs to satisy the requirements to include:

- Employee personal and employment data
- Related active Claims data
- Related active Policies data

Luckily, we have such APIs:

- GET /v1/employees
- POST /v1/policies
- POST /v1/claims

See full [OAS definition](/definitions/complete-oas.json) to see docs or run this repository.

While investigating those API, we need to make sure they support requested pagination, filtering, and sorting.

## URL

Knowing pagination and sorting, we can design URL (method, path, query parameters):

```HTTP
POST /v1/employer/employees?offset=0&limit=10&sort_by=lastName&order=asc
```

I would sugget following the pagination and sorting pattern used by internal APIs. However, it is possible to apply different patterns.

We use POST as GET doesn't imply having a request body. Having multiple filters in URL can reach a limit and cause 414 HTTP error.

## Request Body

Knowing input parameters and required filters, we can construct a request body:

```JSON
{
    "employerId": "913ec1e3-4952-31a6-a24d-9ff71794ae40", // required; Employee:@query/employerId
    "filters": { // optional
        "employeeNumber": "EE1023394", // Employee:@query/businessId
        "firstName": "John", // Employee:@query/firstName
        "lastName": "Doe", // Employee:@query/lastName
        "division": "R&D", // Employee:@query/department
        "position": "Scrum Master", // Employee:@query/position; also reffered as "Title", but we keep consistency
        "employmentType": "FULL-TIME" // custom filtering
    }
}
```

Notes:

- "employerId" can be omitted if sent as a part of a Security Token
- filtering by "employeeType" is not supported by an internal API, but the gateway/BFF layer might have a capability to make filtering on their level

## Response Body

Now we can construct a response body mapping different sources.

HTTP code 200:

```JSON
{
    "result": [
        { // Employee API: "GET /v1/employees" 
            "employeeNumber": "EE1023394", // Employee:businessId
            "firstName": "John",
            "lastName": "Doe",
            "division": "R&D", // Employe:department; where Employee:employmentInfo.employerRef == employerId
            "position": "Scrum Master", // where Employee:employmentInfo.employerRef == employerId
            "employmentType": "FULL-TIME", // where Employee:employmentInfo.employerRef == employerId
            "employeeId": "35376743-84d8-4f69-bb10-3eb54830b5d1", // Employee:id - might be required for further calls
            "claims": [ // Claim Search API: "POST /v1/claims"
                {
                    "claimId": "C109109", // Claim:businessId
                    "effectiveDate": "2023-11-08"
                }
            ],
            "policies": [ // Policy search API: "POST /v1/policies"
                {
                    "policyId": "P109109", // Policy:businessId
                    "effectiveDate": "2023-11-08"
                }
            ]
        }
    ],
    "pagination": {
        "offset": 0,
        "limit": 10
    }
}
```

Notes:

- Internal Employee API model has "employementInfo" as an array, as an Employee might have more than one Employer. For an Experience search, we need to return data related to a current Employer only.

## Request Logic

### Step 1. Call Employee search

```HTTP
GET /v1/employees?employerId={@body/employerId}&status=ACTIVE
```

Other input data is defined in the URL and Request Body section

### Step 2.1 Call Policy Search to get a businessId

Step 2.1 and 2.2 can be done in parallel.

So we call to retun up to 5 active Policies associared with an Employee:

```HTTP
POST /v1/policies?limit=5
```

Request Body

```JSON
{
    "id": [
        "3fa85f64-5717-4562-b3fc-2c963f66afa6" // from Step 1 response result[].policies[].policyRef
    ],
    "status": [
        "ACTIVE"
    ]
}
```

Notes:

- Policy model does not contain a reference to an Employee, so that will be a bulk call with multiple Policy UUIDs coming from the Employee list. In case of a big number of UUIDs the performance may suffer. However pagination and the common sense should help to avoid that.

### Step 2.2 Call Claims Search

Call to retrieve up to 5 Claims associated with an Employee:

```HTTP
POST /v1/claims?limit=5
```

Request body:

```JSON
{
   "claimantRef": [
    "3fa85f64-5717-4562-b3fc-2c963f66afa6"
  ],
  "status": [
    "ACTIVE"
  ]
}
```

Notes:

- Claim model, compared to Policy, has a reference to an Employee. But that will be again a bulk API call with multiple "claimantRef" values. In case of a huge number, the performance may suffer as well.

## Error handling

- No Employees found -> return "result[]"
- No active claims -> return "result[].claims[]"
- No active policies -> return "result[].policies[]"
- Claims Search API unavailable -> return "result[].claims" = null
- Policy Search API unavailable -> return "result[].policies" = null
- Rate-limiter: 5 attempts
- Time-out: 300s
