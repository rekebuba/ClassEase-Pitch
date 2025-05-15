-- prepares a MySQL server for the project

DROP DATABASE IF EXISTS classease_dev_db;
DROP DATABASE IF EXISTS classease_test_db;

DROP USER IF EXISTS 'classease_dev'@'%';
DROP USER IF EXISTS 'classease_test'@'%';

CREATE DATABASE IF NOT EXISTS classease_dev_db;
CREATE DATABASE IF NOT EXISTS classease_test_db;

CREATE USER IF NOT EXISTS 'classease_dev'@'%' IDENTIFIED BY 'key_dev_pwd';
CREATE USER IF NOT EXISTS 'classease_test'@'%' IDENTIFIED BY 'key_test_pwd';

GRANT ALL PRIVILEGES ON classease_dev_db.* TO 'classease_dev'@'%';
GRANT ALL PRIVILEGES ON classease_test_db.* TO 'classease_test'@'%';

GRANT SELECT ON performance_schema.* TO 'classease_dev'@'%';
GRANT SELECT ON performance_schema.* TO 'classease_test'@'%';

FLUSH PRIVILEGES;
