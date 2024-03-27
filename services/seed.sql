USE clinic;

DELETE FROM clinic;
INSERT INTO clinic (clinicID, clinicName, location, services) VALUES
('clinic1', 'Healing Hands', 'New York', '[\"General Checkup\", \"Pediatrics\"]'),
('clinic2', 'MediCare Clinic', 'Los Angeles', '[\"Dermatology\", \"Neurology\"]'),
('clinic3', 'Wellness Center', 'Chicago', '[\"Cardiology\", \"ENT\"]'),
('clinic4', 'Quick Heal', 'Houston', '[\"Orthopedics\", \"Dentistry\"]'),
('clinic5', 'Prime Health Solutions', 'Phoenix', '[\"Gynecology\", \"Ophthalmology\"]'),
('clinic6', 'Family Health Clinic', 'Philadelphia', '[\"General Practice\", \"Pediatrics\"]'),
('clinic7', 'Community Care Clinic', 'San Antonio', '[\"Mental Health\", \"General Practice\"]'),
('clinic8', 'Advanced Medical Center', 'San Diego', '[\"Cardiology\", \"Orthopedics\"]'),
('clinic9', 'Metro Health Clinic', 'Dallas', '[\"Neurology\", \"General Practice\"]'),
('clinic10', 'Pioneer Health Services', 'San Jose', '[\"Endocrinology\", \"Dermatology\"]');

USE profile;

DELETE FROM patient;
INSERT INTO patient (patientID, email, password, patientName, contactNum) VALUES
('patient1', 'john.doe@example.com', 'password1', 'John Doe', 12345678),
('patient2', 'jane.smith@example.com', 'password2', 'Jane Smith', 23456789),
('patient3', 'mike.brown@example.com', 'password3', 'Mike Brown', 34567890),
('patient4', 'sarah.connor@example.com', 'password4', 'Sarah Connor', 45678901),
('patient5', 'david.tennant@example.com', 'password5', 'David Tennant', 56789012),
('patient6', 'jessica.jones@example.com', 'password6', 'Jessica Jones', 67890123),
('patient7', 'michael.scott@example.com', 'password7', 'Michael Scott', 78901234),
('patient8', 'pam.beesly@example.com', 'password8', 'Pam Beesly', 89012345),
('patient9', 'jim.halpert@example.com', 'password9', 'Jim Halpert', 90123456),
('patient10', 'dwight.schrute@example.com', 'password10', 'Dwight Schrute', 10123456);

USE profile;

DELETE FROM doctor;
INSERT INTO doctor (doctorID, clinicID, email, password, doctorName, doctorDesc, specialty) VALUES
('doctor1', 'clinic1', 'doc1@example.com', 'pass1', 'Dr. Alice Jones', 'Experienced General Practitioner', 'General Practice'),
('doctor2', 'clinic2', 'doc2@example.com', 'pass2', 'Dr. Bob Smith', 'Cardiology Specialist', 'Cardiology'),
('doctor3', 'clinic3', 'doc3@example.com', 'pass3', 'Dr. Charlie Day', 'Expert in Dermatology', 'Dermatology'),
('doctor4', 'clinic4', 'doc4@example.com', 'pass4', 'Dr. Dana Scully', 'Renowned Neurologist', 'Neurology'),
('doctor5', 'clinic5', 'doc5@example.com', 'pass5', 'Dr. Ethan Hunt', 'Orthopedics Specialist', 'Orthopedics'),
('doctor6', 'clinic1', 'doc6@example.com', 'pass6', 'Dr. Fiona Gallagher', 'Pediatrics Expert', 'Pediatrics'),
('doctor7', 'clinic2', 'doc7@example.com', 'pass7', 'Dr. George Costanza', 'Dentistry Specialist', 'Dentistry'),
('doctor8', 'clinic3', 'doc8@example.com', 'pass8', 'Dr. Hank Moody', 'Cardiology Expert', 'Cardiology'),
('doctor9', 'clinic4', 'doc9@example.com', 'pass9', 'Dr. Ian Malcolm', 'General Practice Expert', 'General Practice'),
('doctor10', 'clinic5', 'doc10@example.com', 'pass10', 'Dr. Jane Foster', 'Specialist in Ophthalmology', 'Ophthalmology');

USE blocked_slots;

DELETE FROM blocked_slots;
INSERT INTO blocked_slots (id, doctorID, clinicID, date, slotNo, reason) VALUES
('blockedSlotID1', 'doctor1', 'clinic1', '2024-01-10', 9, 'Maintenance'),
('blockedSlotID2', 'doctor2', 'clinic1', '2024-01-11', 10, 'Personal Leave'),
('blockedSlotID3', 'doctor3', 'clinic2', '2024-01-12', 11, 'Conference'),
('blockedSlotID4', 'doctor4', 'clinic2', '2024-01-13', 12, 'Maintenance'),
('blockedSlotID5', 'doctor5', 'clinic3', '2024-01-14', 13, 'Personal Leave'),
('blockedSlotID6', 'doctor6', 'clinic3', '2024-01-15', 14, 'Conference'),
('blockedSlotID7', 'doctor7', 'clinic4', '2024-01-16', 15, 'Maintenance'),
('blockedSlotID8', 'doctor8', 'clinic4', '2024-01-17', 16, 'Personal Leave'),
('blockedSlotID9', 'doctor9', 'clinic5', '2024-01-18', 17, 'Conference'),
('blockedSlotID10', 'doctor10', 'clinic5', '2024-01-19', 18, 'Maintenance');

USE booking;

DELETE FROM booking;
INSERT INTO booking (bookingID, patientID, clinicID, doctorID, date, slotNo, bookingStatus) VALUES
('booking1', 'patient1', 'clinic1', 'doctor1', '2024-01-20', 8, 'Confirmed'),
('booking2', 'patient2', 'clinic1', 'doctor2', '2024-01-21', 9, 'Confirmed'),
('booking3', 'patient3', 'clinic2', 'doctor3', '2024-01-22', 10, 'Confirmed'),
('booking4', 'patient4', 'clinic2', 'doctor4', '2024-01-23', 11, 'Confirmed'),
('booking5', 'patient5', 'clinic3', 'doctor5', '2024-01-24', 12, 'Confirmed'),
('booking6', 'patient6', 'clinic3', 'doctor6', '2024-01-25', 13, 'Confirmed'),
('booking7', 'patient7', 'clinic4', 'doctor7', '2024-01-26', 14, 'Confirmed'),
('booking8', 'patient8', 'clinic4', 'doctor8', '2024-01-27', 15, 'Confirmed'),
('booking9', 'patient9', 'clinic5', 'doctor9', '2024-01-28', 16, 'Confirmed'),
('booking10', 'patient10', 'clinic5', 'doctor10', '2024-01-29', 17, 'Confirmed');

USE rating;

DELETE FROM doctor_rating;
INSERT INTO doctor_rating (ratingID, clinicID, doctorID, bookingID, patientID, ratingGiven, comments, timeStamp) VALUES
('rating1', 'clinic1', 'doctor1', 'booking1', 'patient1', 4.8, 'Excellent service', CURRENT_TIMESTAMP),
('rating2', 'clinic1', 'doctor2', 'booking2', 'patient2', 4.5, 'Very professional', CURRENT_TIMESTAMP),
('rating3', 'clinic2', 'doctor3', 'booking3', 'patient3', 4.7, 'Friendly and understanding', CURRENT_TIMESTAMP),
('rating4', 'clinic2', 'doctor4', 'booking4', 'patient4', 4.9, 'Outstanding care', CURRENT_TIMESTAMP),
('rating5', 'clinic3', 'doctor5', 'booking5', 'patient5', 4.6, 'Very thorough', CURRENT_TIMESTAMP),
('rating6', 'clinic3', 'doctor6', 'booking6', 'patient6', 4.4, 'Good, but a bit rushed', CURRENT_TIMESTAMP),
('rating7', 'clinic4', 'doctor7', 'booking7', 'patient7', 4.3, 'Decent service', CURRENT_TIMESTAMP),
('rating8', 'clinic4', 'doctor8', 'booking8', 'patient8', 4.5, 'Very knowledgeable', CURRENT_TIMESTAMP),
('rating9', 'clinic5', 'doctor9', 'booking9', 'patient9', 4.8, 'Exceptional bedside manner', CURRENT_TIMESTAMP),
('rating10', 'clinic5', 'doctor10', 'booking10', 'patient10', 4.7, 'Professional and kind', CURRENT_TIMESTAMP);
