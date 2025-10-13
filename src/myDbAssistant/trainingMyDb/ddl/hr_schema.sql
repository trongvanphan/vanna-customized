-- HR Schema Tables
-- Oracle Database DDL for Human Resources Schema

-- Employees Table
CREATE TABLE employees (
    employee_id NUMBER(6) PRIMARY KEY,
    first_name VARCHAR2(20),
    last_name VARCHAR2(25) NOT NULL,
    email VARCHAR2(25) NOT NULL,
    phone_number VARCHAR2(20),
    hire_date DATE NOT NULL,
    job_id VARCHAR2(10) NOT NULL,
    salary NUMBER(8,2),
    commission_pct NUMBER(2,2),
    manager_id NUMBER(6),
    department_id NUMBER(4)
);

-- Departments Table
CREATE TABLE departments (
    department_id NUMBER(4) PRIMARY KEY,
    department_name VARCHAR2(30) NOT NULL,
    manager_id NUMBER(6),
    location_id NUMBER(4)
);

-- Jobs Table
CREATE TABLE jobs (
    job_id VARCHAR2(10) PRIMARY KEY,
    job_title VARCHAR2(35) NOT NULL,
    min_salary NUMBER(6),
    max_salary NUMBER(6)
);

-- Comments
COMMENT ON TABLE employees IS 'Employee information including personal details, job, and salary';
COMMENT ON TABLE departments IS 'Department information including name and manager';
COMMENT ON TABLE jobs IS 'Job roles with salary ranges';

-- Indexes (optional, for performance)
CREATE INDEX emp_department_ix ON employees(department_id);
CREATE INDEX emp_job_ix ON employees(job_id);
CREATE INDEX emp_manager_ix ON employees(manager_id);
CREATE INDEX dept_manager_ix ON departments(manager_id);
