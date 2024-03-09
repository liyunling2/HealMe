CREATE DATABASE IF NOT EXISTS blocked_slots;

CREATE USER IF NOT EXISTS 'blocked_slots'@'localhost' IDENTIFIED BY 'blocked_slots';
GRANT ALL PRIVILEGES ON blocked_slots.* TO 'blocked_slots'@'localhost';

CREATE DATABASE IF NOT EXISTS `profile`;

CREATE USER IF NOT EXISTS 'profile'@'localhost' IDENTIFIED BY 'profile';
GRANT ALL PRIVILEGES ON profile.* TO 'profile'@'localhost';

CREATE DATABASE IF NOT EXISTS `clinic`;

CREATE USER IF NOT EXISTS 'clinic'@'localhost' IDENTIFIED BY 'clinic';
GRANT ALL PRIVILEGES ON clinic.* TO 'clinic'@'localhost';