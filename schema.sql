-- Weather App Database Schema
-- Railway MySQL

CREATE DATABASE IF NOT EXISTS weatherdb;
USE weatherdb;

CREATE TABLE IF NOT EXISTS search_history (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    city        VARCHAR(100) NOT NULL,
    country     VARCHAR(10),
    temperature FLOAT,
    description VARCHAR(200),
    humidity    INT,
    wind_speed  FLOAT,
    searched_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Sample data
INSERT INTO search_history (city, country, temperature, description, humidity, wind_speed)
VALUES
  ('Kampala',  'UG', 24.5, 'Partly Cloudy', 78, 3.2),
  ('London',   'GB', 12.1, 'Overcast Clouds', 85, 5.7),
  ('Nairobi',  'KE', 21.3, 'Light Rain', 72, 2.8),
  ('New York', 'US', 18.6, 'Clear Sky', 55, 4.1);