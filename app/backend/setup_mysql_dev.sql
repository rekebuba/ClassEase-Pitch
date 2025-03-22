-- prepares a MySQL server for the project

DROP DATABASE IF EXISTS classease;

CREATE DATABASE IF NOT EXISTS classease;

CREATE USER IF NOT EXISTS 'classease_dev' @'localhost' IDENTIFIED BY 'key_dev_pwd';

GRANT ALL PRIVILEGES ON `classease`.* TO 'classease_dev' @'localhost';

GRANT
SELECT ON `performance_schema`.* TO 'classease_dev' @'localhost';

FLUSH PRIVILEGES;
