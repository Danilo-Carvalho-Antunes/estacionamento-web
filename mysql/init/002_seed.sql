USE estac_db;

-- Contractor
INSERT INTO contractors (name) VALUES ('Acme Parking')
  ON DUPLICATE KEY UPDATE name = VALUES(name);

SET @contractor_id = (SELECT id FROM contractors WHERE name='Acme Parking');

-- Parking lots
INSERT INTO parking_lots (contractor_id, name, open_at, close_at, capacity) VALUES
  (@contractor_id, 'Centro', '06:00:00', '22:00:00', 120),
  (@contractor_id, 'Aeroporto', '00:00:00', '23:59:59', 300)
ON DUPLICATE KEY UPDATE open_at=VALUES(open_at), close_at=VALUES(close_at), capacity=VALUES(capacity);

SET @lot_centro = (SELECT id FROM parking_lots WHERE contractor_id=@contractor_id AND name='Centro');
SET @lot_aeroporto = (SELECT id FROM parking_lots WHERE contractor_id=@contractor_id AND name='Aeroporto');

-- Pricing profiles
INSERT INTO pricing_profiles (parking_lot_id, name, fraction_minutes, fraction_rate, hourly_rate, daily_rate, nightly_rate) VALUES
  (@lot_centro, 'Padrão', 15, 5.00, 12.00, 70.00, 50.00),
  (@lot_aeroporto, 'Padrão', 15, 6.00, 14.00, 80.00, 55.00)
ON DUPLICATE KEY UPDATE fraction_minutes=VALUES(fraction_minutes), fraction_rate=VALUES(fraction_rate), hourly_rate=VALUES(hourly_rate), daily_rate=VALUES(daily_rate), nightly_rate=VALUES(nightly_rate);

-- Vehicles
INSERT IGNORE INTO vehicles (plate, owner_name) VALUES
  ('ABC1A23','João Silva'),
  ('DEF2B34','Maria Souza'),
  ('GHI3C45','Pedro Santos'),
  ('JKL4D56','Ana Lima'),
  ('MNO5E67','Carlos Pereira'),
  ('PQR6F78','Marina Costa'),
  ('STU7G89','Bruno Alves'),
  ('VWX8H90','Renata Dias'),
  ('YZA9I01','Tiago Rocha'),
  ('BCA0J12','Laura Mendes');

-- Events
INSERT INTO events (parking_lot_id, name, starts_at, ends_at, price) VALUES
  (@lot_centro, 'Show na Praça', '2024-06-15 18:00:00.000000', '2024-06-15 23:59:59.000000', 40.00),
  (@lot_aeroporto, 'Feira Aero', '2024-07-20 08:00:00.000000', '2024-07-20 20:00:00.000000', 60.00)
ON DUPLICATE KEY UPDATE price=VALUES(price), ends_at=VALUES(ends_at);

-- Vehicle IDs
SET @veh1 = (SELECT id FROM vehicles WHERE plate='ABC1A23');
SET @veh2 = (SELECT id FROM vehicles WHERE plate='DEF2B34');
SET @veh3 = (SELECT id FROM vehicles WHERE plate='GHI3C45');
SET @veh4 = (SELECT id FROM vehicles WHERE plate='JKL4D56');
SET @veh5 = (SELECT id FROM vehicles WHERE plate='MNO5E67');

-- Accesses (idempotent via UNIQUE(vehicle_id, start_at))
INSERT IGNORE INTO accesses (vehicle_id, parking_lot_id, start_at, end_at, price, status) VALUES
  (@veh1, @lot_centro, '2024-06-10 09:10:00.000000', '2024-06-10 10:05:00.000000', 12.00, 'closed'),
  (@veh2, @lot_centro, '2024-06-10 17:50:00.000000', '2024-06-10 19:20:00.000000', 20.00, 'closed'),
  (@veh3, @lot_aeroporto, '2024-07-21 22:10:00.000000', NULL, NULL, 'open'),
  (@veh4, @lot_aeroporto, '2024-07-21 07:35:00.000000', '2024-07-21 10:05:00.000000', 25.00, 'closed'),
  (@veh5, @lot_centro, '2024-06-11 12:00:00.000000', '2024-06-11 18:30:00.000000', 70.00, 'closed');
