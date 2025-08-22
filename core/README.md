# FarmHub - Farm Management Platform (Core Service)

A comprehensive farm management platform built with Django and Django REST Framework, designed to manage farms, farmers, cows, activities, and milk production with role-based access control.

## Overview

FarmHub provides a solution for farm management with:
- **User Management**: SuperAdmins, Agents, and Farmers with role-based permissions
- **Farm Management**: Registration and management of farms with assigned agents
- **Cow Management**: Cow enrollment with unique tags per farm
- **Activity Tracking**: Health activities, vaccinations, births, and general care
- **Milk Production**: Daily milk recording with aggregation and reporting
- **Admin Interface**: Enhanced Django admin with search, filters, and inline editing


## Setup Instructions

1. Clone and navigate to project:
   ```bash
   cd /path/to/FarmHub/core
   ```
2. Create and activate virtual environment:
   ```bash
   python -m venv .venv
   source .venv/Scripts/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
5. Load seed data:
   ```bash
   python manage.py shell < management_seed.py
   ```
6. Start server:
   ```bash
   python manage.py runserver
   ```

## Data Model

**User**
- username (unique)
- email
- role: superadmin | agent | farmer

**Farm**
- name
- location
- agent (User)

**Cow**
- tag (unique per farm)
- breed
- farm (Farm)
- owner (User)

**Activity**
- cow (Cow)
- performed_by (User)
- activity_type
- date

**MilkRecord**
- cow (Cow)
- recorded_by (User)
- date
- quantity_liters

## Role Design

- **SuperAdmin**: Full access
- **Agent**: Manages assigned farms, onboard farmers
- **Farmer**: Manages own cows, activities, milk records

## Example API Calls

**Get Auth Token**
```bash
curl -X POST http://127.0.0.1:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"superadmin","password":"password"}'
```

**Get Current User**
```bash
curl -H "Authorization: Token YOUR_TOKEN" \
  http://127.0.0.1:8000/api/users/me/
```

**Onboard Farmer**
```bash
curl -X POST http://127.0.0.1:8000/api/users/onboard_farmer/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"username":"farmer2","password":"password","email":"farmer2@example.com"}'
```

**Create Farm**
```bash
curl -X POST http://127.0.0.1:8000/api/farms/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"Blue Farm","location":"Mountain Valley"}'
```

**Enroll Cow**
```bash
curl -X POST http://127.0.0.1:8000/api/cows/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"tag":"COW-003","breed":"Holstein","farm":1}'
```

**Log Activity**
```bash
curl -X POST http://127.0.0.1:8000/api/activities/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"cow":1,"activity_type":"vaccination","notes":"Annual vaccination","date":"2025-08-22"}'
```

**Record Milk**
```bash
curl -X POST http://127.0.0.1:8000/api/milk/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"cow":1,"date":"2025-08-22","quantity_liters":"15.5"}'
```

**Get Milk Aggregation**
```bash
curl -H "Authorization: Token YOUR_TOKEN" \
  "http://127.0.0.1:8000/api/milk/aggregate/?start=2025-08-01&end=2025-08-31"
```

# Get milk aggregation by date range
curl -H "Authorization: Token YOUR_TOKEN" \
  "http://127.0.0.1:8000/api/milk/aggregate/?start=2025-08-01&end=2025-08-31"

# Get milk totals by farm (agent/superadmin only)
curl -H "Authorization: Token YOUR_TOKEN" \
  "http://127.0.0.1:8000/api/milk/by_farm/?start=2025-08-01&end=2025-08-31"
```