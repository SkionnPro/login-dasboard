CREATE DATABASE IF NOT EXISTS client_registrations;
USE client_registrations;

CREATE TABLE IF NOT EXISTS clients(
  id INT AUTO_INCREMENT PRIMARY KEY,
  first_name VARCHAR(50),
  last_name VARCHAR(50),
  register_as VARCHAR(50),
  company_name VARCHAR(100),
  email VARCHAR(100) UNIQUE,
  mobile_number VARCHAR(15),
  password VARCHAR(255),
  client_id VARCHAR(100) DEFAULT NULL,
  client_secret VARCHAR(100) DEFAULT NULL
);