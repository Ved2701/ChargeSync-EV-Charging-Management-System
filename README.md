# ChargeSync – EV Charging Management System

A centralized EV charging management system built using Python, Tkinter, and MySQL to manage EV owners, charging stations, slot bookings, payments, maintenance requests, and power allocation through a database-driven desktop application.

The project was developed as part of a DBMS course project to model real-world EV charging operations while demonstrating relational schema design, SQL queries, triggers, transactions, and concurrency handling in a multi-user environment.

## Features

### EV Owner & Vehicle Management
- EV owner registration with personal details
- Multiple vehicle registration under a single owner
- Vehicle details including registration number, type, and battery capacity

### Charging Station & Slot Management
- Charging station management with operator details
- Charging slot availability tracking
- Slot booking with date and duration selection
- Prevention of double booking using database triggers

### Power Allocation & Monitoring
- Track allocated and available power at charging stations
- Threshold-based power monitoring
- Operator-controlled power updates
- Designed to support real-world EV charging infrastructure workflows

### Payments & Billing
- Payment tracking based on charging sessions
- Energy consumption recording
- Revenue and usage analytics using SQL queries

### Maintenance & Vendor Handling
- Vendor registration and maintenance request management
- Maintenance request tracking for charging stations

### Transactions & Concurrency Handling
- Concurrent transaction handling using row-level locking (`SELECT ... FOR UPDATE`)
- Commit and rollback mechanisms
- Conflict detection during simultaneous updates
- Demonstration of ACID properties and database consistency

## Database Design Highlights

- Normalized relational schema with 10+ interconnected entities
- Primary and foreign key constraints
- Trigger-based integrity enforcement
- Use of joins, aggregations, subqueries, and analytical SQL queries
- Transaction management with concurrency control

## Tech Stack

- Language: Python
- GUI: Tkinter
- Database: MySQL
- Concepts: SQL, Transactions, Triggers, Concurrency Control, Row-Level Locking

## Key SQL Features Demonstrated

- Joins and Multi-table Joins
- Aggregation and Group By
- HAVING clauses
- Subqueries
- Trigger-based validations
- Transactions with COMMIT / ROLLBACK
- Row-level locking using `SELECT FOR UPDATE`

## Learning Outcomes

- Designed and implemented a real-world relational database system
- Applied DBMS concepts including normalization, constraints, triggers, and transactions
- Understood concurrency handling and ACID properties in multi-user systems
- Built a GUI-driven application integrated with MySQL
- Gained practical experience in database-backed application development

## Setup Instructions

1. Import the sql file into MySQL
2. Update database credentials in the python file
3. Run the application

## Notes

This project uses simulated data for demonstration purposes while being designed around realistic EV charging workflows and scalable database operations.
