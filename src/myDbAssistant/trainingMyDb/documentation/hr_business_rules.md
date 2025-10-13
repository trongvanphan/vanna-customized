# HR Database Business Rules and Documentation

## Overview
This database contains Human Resources data for employee management, including employee information, departments, and job roles.

## Business Rules

### Salaries
- All salaries are in **USD**
- Salary amounts are stored with 2 decimal places (e.g., 50000.00)
- `commission_pct` represents commission as a percentage from 0.0 to 1.0
  - Example: 0.25 = 25% commission
  - NULL means no commission

### Fiscal Year
- The fiscal year starts in **January** (January 1st)
- Hire dates use standard DATE format

### Employee IDs
- Employee IDs are **6-digit numbers**
- Format: NUMBER(6) - e.g., 100001, 100002, etc.
- Employee IDs are unique and auto-generated

### Relationships

#### Employees Table
- `department_id` references the `departments` table
  - NULL means employee is not assigned to a department
- `manager_id` references another employee in the `employees` table
  - Self-referencing foreign key
  - NULL means employee has no manager (typically executives)
- `job_id` references the `jobs` table
  - Defines the employee's role and salary range

#### Departments Table
- `manager_id` references an employee who manages the department
- `location_id` would reference a locations table (if implemented)

### Data Validation Rules
1. `last_name` is required (NOT NULL)
2. `email` is required and should be unique (NOT NULL)
3. `hire_date` is required (NOT NULL)
4. `job_id` is required (NOT NULL)
5. `salary` should be within the min/max range defined in the `jobs` table

## Common Queries

### Employee Queries
- Find employees by name, department, or job title
- Calculate total compensation (salary + commission)
- Find reporting hierarchy (manager-employee relationships)

### Department Queries
- Count employees per department
- Calculate average/total salary per department
- Find departments without managers or employees

### Salary Queries
- Top earners (highest salaries)
- Salary ranges by job title
- Commission analysis

## Data Dictionary

### Employees Table Columns
- `employee_id`: Unique identifier for each employee
- `first_name`: Employee's first name (optional)
- `last_name`: Employee's last name (required)
- `email`: Employee's email address (required, unique)
- `phone_number`: Contact phone number (optional)
- `hire_date`: Date employee was hired (required)
- `job_id`: Job role identifier (required)
- `salary`: Monthly or annual salary in USD (optional)
- `commission_pct`: Commission percentage 0.0-1.0 (optional)
- `manager_id`: Employee ID of direct manager (optional)
- `department_id`: Department assignment (optional)

### Departments Table Columns
- `department_id`: Unique identifier for department
- `department_name`: Name of the department (required)
- `manager_id`: Employee ID of department manager (optional)
- `location_id`: Location identifier (optional)

### Jobs Table Columns
- `job_id`: Unique identifier for job role
- `job_title`: Name of the job role (required)
- `min_salary`: Minimum salary for this role (optional)
- `max_salary`: Maximum salary for this role (optional)

## Notes for AI/LLM
- When querying employees, use schema prefix: `hr.employees`
- For salary queries, handle NULL commission_pct gracefully
- For hierarchical queries (managers), use self-joins on employees table
- For department counts, use LEFT JOIN to include departments with no employees
- Oracle uses `FETCH FIRST n ROWS ONLY` instead of `LIMIT n`
- Date format in Oracle: `TO_DATE('YYYY-MM-DD', 'YYYY-MM-DD')`
