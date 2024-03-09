CREATE DATABASE IF NOT EXISTS blocked_slots;

CREATE USER IF NOT EXISTS 'blocked_slots'@'%' IDENTIFIED BY 'blocked_slots';
GRANT ALL PRIVILEGES ON blocked_slots.* TO 'blocked_slots'@'%';

CREATE DATABASE IF NOT EXISTS `profile`;

CREATE USER IF NOT EXISTS 'profile'@'%' IDENTIFIED BY 'profile';
GRANT ALL PRIVILEGES ON profile.* TO 'profile'@'%';

CREATE DATABASE IF NOT EXISTS `clinic`;

CREATE USER IF NOT EXISTS 'clinic'@'%' IDENTIFIED BY 'clinic';
GRANT ALL PRIVILEGES ON clinic.* TO 'clinic'@'%';