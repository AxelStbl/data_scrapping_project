CREATE DATABASE IF NOT EXISTS scrapping;
ALTER DATABASE scrapping CHARACTER SET utf8 COLLATE utf8_general_ci;
USE scrapping;
SET collation_connection = 'utf8_general_ci';

CREATE TABLE IF NOT EXISTS companies (
  id int PRIMARY KEY AUTO_INCREMENT,
  name varchar(255) UNIQUE NOT NULL,
  headquarters_city varchar(255),
  headquarters_country varchar(255),
  headquarters_currency varchar(255),
  rating float,
  rating_count int,
  benefits_rating float,
  benefits_rating_count int,
  nb_of_employees varchar(255),
  founded int,
  type varchar(255),
  website varchar(255),
  competitors varchar(255)
);
ALTER TABLE companies CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;

CREATE TABLE IF NOT EXISTS job_offers (
  id int PRIMARY KEY AUTO_INCREMENT,
  job_id BIGINT UNIQUE NOT NULL,
  city varchar(255),
  position varchar(255),
  company_id int,
  description varchar(255),
  salary int,
  FOREIGN KEY (company_id) REFERENCES companies (id)
);
ALTER TABLE job_offers CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;