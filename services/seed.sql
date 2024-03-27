USE profile;

DELETE FROM doctor;
INSERT INTO doctor

-- CREATE TABLE `doctor` (
--   `doctorID` varchar(36) NOT NULL,
--   `clinicID` varchar(36) DEFAULT NULL,
--   `doctorName` varchar(255) DEFAULT NULL,
--   `doctorDesc` varchar(255) DEFAULT NULL,
--   `specialty` varchar(255) DEFAULT NULL,
--   `ratings` float DEFAULT NULL,
--   PRIMARY KEY (`doctorID`)
-- )

VALUES
("doctor1", "clinic1", "Dr. John Doe", "General Practitioner", "Family Medicine", 4.5),
("doctor2", "clinic1", "Dr. Jane Smith", "Cardiologist", "Internal Medicine", 4.8),
("doctor3", "clinic2", "Dr. David Johnson", "Dermatologist", "Dermatology", 4.2);

--  CREATE TABLE `patient` (
--   `patientID` varchar(36) NOT NULL,
--   `patientName` varchar(255) DEFAULT NULL,
--   `contactNum` int DEFAULT NULL,
--   `allergies` text,
--   `medications` text,
--   PRIMARY KEY (`patientID`)
-- )

DELETE FROM patient;
INSERT INTO patient
VALUES
("patient1", "John Smith", 1234567890, JSON_ARRAY("Peanuts", "Gluten"), JSON_ARRAY("Aspirin")),
("patient2", "Jane Doe", 1234567890, JSON_ARRAY("Shellfish", "Gluten"), JSON_ARRAY("Penicillin")),
("patient3", "David Johnson", 1234567890, JSON_ARRAY("Pollen", "Gluten"), JSON_ARRAY("Ibuprofen"));


USE clinic;

-- CREATE TABLE `clinic` (
--   `clinicID` varchar(36) NOT NULL,
--   `clinicName` varchar(255) DEFAULT NULL,
--   `location` varchar(255) DEFAULT NULL,
--   `services` text,
--   PRIMARY KEY (`clinicID`)
-- )

DELETE FROM clinic;
INSERT INTO clinic
VALUES
("clinic1", "General Hospital", "123 Main St, New York, NY 10001", "General Medicine, Cardiology, Dermatology"),
("clinic2", "St. Mary's Hospital", "456 Elm St, New York, NY 10002", "Cardiology, Dermatology"),
("clinic3", "St. Joseph's Hospital", "789 Oak St, New York, NY 10003", "Dermatology");

-- USE booking;

-- -- CREATE TABLE `booking` (
-- --   `bookingID` varchar(36) NOT NULL,
-- --   `patientID` varchar(36) DEFAULT NULL,
-- --   `doctorID` varchar(36) DEFAULT NULL,
-- --   `clinicID` varchar(36) DEFAULT NULL,
-- --   `date` datetime DEFAULT NULL,
-- --   `slotNo` int DEFAULT NULL,
-- --   `bookingStatus` varchar(255) DEFAULT NULL,
-- --   PRIMARY KEY (`bookingID`),
-- --   UNIQUE KEY `doctorID_date_slotNo` (`doctorID`,`date`,`slotNo`),
-- --   CONSTRAINT `slotNo_check` CHECK (((`slotNo` >= 1) and (`slotNo` <= 24)))
-- -- )

-- DELETE from booking;
-- INSERT INTO booking
-- VALUES
-- ("b0o1o2k3i4n5g6", "p0a1t2i3e4n5t6i7d8", "c0bda65c-93c1-4621-ad38-164f5be3db5f", "c0bda65c-93c1-4621-ad38-164f5be3db5f", "2021-01-01", 1, "Confirmed"),
-- ("b7o8o9k0i1n2g3", "p9a0t1i2e3n4t5i6d7", "d8e9f0a1-b2c3-d4e5-f6g7-h8i9j0k1l2m3", "d8e9f0a1-b2c3-d4e5-f6g7-h8i9j0k1l2m3", "2021-01-01", 2, "Confirmed"),
-- ("b9o0o1k2i3n4g5", "p8a7t6i5e4n3t2i1d0", "n2m3l4k5-j6i7h8-g9f0e1d2c3b4", "n2m3l4k5-j6i7h8-g9f0e1d2c3b4", "2021-01-01", 3, "Confirmed");


