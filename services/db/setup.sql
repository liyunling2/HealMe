CREATE DATABASE IF NOT EXISTS schedule;

CREATE USER IF NOT EXISTS 'schedule'@'localhost' IDENTIFIED BY 'schedule';
GRANT ALL PRIVILEGES ON schedule.* TO 'schedule'@'localhost';

CREATE DATABASE IF NOT EXISTS `profile`;

CREATE USER IF NOT EXISTS 'profile'@'localhost' IDENTIFIED BY 'profile';
GRANT ALL PRIVILEGES ON profile.* TO 'profile'@'localhost';
