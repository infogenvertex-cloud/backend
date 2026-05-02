-- Setup script for TiDB Cloud
-- Run this in TiDB Cloud SQL Editor or MySQL client

-- Create database
CREATE DATABASE IF NOT EXISTS gym_db;

-- Use the database
USE gym_db;

-- Verify database is created
SHOW DATABASES;

-- The tables will be created automatically by the FastAPI application
-- when it starts up (via SQLAlchemy Base.metadata.create_all)
