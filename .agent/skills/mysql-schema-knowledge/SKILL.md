---
name: mysql-schema-knowledge
description: Provides knowledge of the MySQL 8 database schema for Spudooli News App. Use when writing SQL queries, debugging data issues, or generating reports.
---

# MySQL Schema Knowledge: Spudooli News App

## Overview
This skill contains the complete DDL schema for the production MySQL 8 database. Use this context to:
- Write accurate SELECT/INSERT/UPDATE queries
- Understand table relationships and foreign keys
- Debug data integrity issues

## Schema Reference
See `resources/schema.md` for the full table definitions.

## Query Guidelines
1. Always use parameterized queries to prevent SQL injection
2. Prefer JOINs over subqueries for readability
3. Include `LIMIT` clauses for exploratory queries
4. Respect soft-delete patterns (`deleted_at IS NULL`)

## Common Patterns
- User lookup: `SELECT * FROM users WHERE email = ?`
- Order history: `JOIN orders ON users.id = orders.user_id`
- Aggregations: Use `GROUP BY` with `COUNT()`, `SUM()`

## Security Notes
- NEVER expose raw schema to end users
