-- Initial schema for estacionamento app
CREATE DATABASE IF NOT EXISTS estac_db CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE estac_db;

-- Contractors
CREATE TABLE IF NOT EXISTS contractors (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY uq_contractors_name (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Parking lots
CREATE TABLE IF NOT EXISTS parking_lots (
  id INT AUTO_INCREMENT PRIMARY KEY,
  contractor_id INT NOT NULL,
  name VARCHAR(255) NOT NULL,
  open_at TIME NOT NULL DEFAULT '06:00:00',
  close_at TIME NOT NULL DEFAULT '22:00:00',
  capacity INT NOT NULL DEFAULT 0,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY uq_parking_lots (contractor_id, name),
  CONSTRAINT fk_parking_lots_contractor FOREIGN KEY (contractor_id) REFERENCES contractors(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Pricing profiles
CREATE TABLE IF NOT EXISTS pricing_profiles (
  id INT AUTO_INCREMENT PRIMARY KEY,
  parking_lot_id INT NOT NULL,
  name VARCHAR(255) NOT NULL,
  fraction_minutes INT NOT NULL DEFAULT 15,
  fraction_rate DECIMAL(10,2) NOT NULL DEFAULT 0.00,
  hourly_rate DECIMAL(10,2) NOT NULL DEFAULT 0.00,
  daily_rate DECIMAL(10,2) NOT NULL DEFAULT 0.00,
  nightly_rate DECIMAL(10,2) NOT NULL DEFAULT 0.00,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY uq_pricing_profiles (parking_lot_id, name),
  CONSTRAINT fk_pricing_profiles_lot FOREIGN KEY (parking_lot_id) REFERENCES parking_lots(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Vehicles
CREATE TABLE IF NOT EXISTS vehicles (
  id INT AUTO_INCREMENT PRIMARY KEY,
  plate VARCHAR(10) NOT NULL,
  owner_name VARCHAR(255),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY uq_vehicles_plate (plate)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Events
CREATE TABLE IF NOT EXISTS events (
  id INT AUTO_INCREMENT PRIMARY KEY,
  parking_lot_id INT NOT NULL,
  name VARCHAR(255) NOT NULL,
  starts_at DATETIME(6) NOT NULL,
  ends_at DATETIME(6) NOT NULL,
  price DECIMAL(10,2) NOT NULL DEFAULT 0.00,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY uq_events (parking_lot_id, name, starts_at),
  CONSTRAINT fk_events_lot FOREIGN KEY (parking_lot_id) REFERENCES parking_lots(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Accesses
CREATE TABLE IF NOT EXISTS accesses (
  id INT AUTO_INCREMENT PRIMARY KEY,
  vehicle_id INT NOT NULL,
  parking_lot_id INT NOT NULL,
  start_at DATETIME(6) NOT NULL,
  end_at DATETIME(6) NULL,
  price DECIMAL(10,2) NULL,
  status ENUM('open','closed') NOT NULL DEFAULT 'open',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY uq_accesses_vehicle_start (vehicle_id, start_at),
  INDEX idx_accesses_parking_lot (parking_lot_id),
  INDEX idx_accesses_vehicle (vehicle_id),
  INDEX idx_accesses_start_at (start_at),
  CONSTRAINT fk_accesses_vehicle FOREIGN KEY (vehicle_id) REFERENCES vehicles(id) ON DELETE RESTRICT,
  CONSTRAINT fk_accesses_lot FOREIGN KEY (parking_lot_id) REFERENCES parking_lots(id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
