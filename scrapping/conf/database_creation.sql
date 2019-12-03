#Run this in local if you want to execute it
#GRANT ALL PRIVILEGES ON *.* TO 'username'@'localhost' IDENTIFIED BY 'password';
#CREATE USER 'username'@'localhost' IDENTIFIED BY PASSWORD 'password';
#GRANT ALL ON *.* TO 'username'@'localhost';
CREATE DATABASE IF NOT EXISTS scrapping;
USE scrapping;

CREATE TABLE IF NOT EXISTS companies (
  id int PRIMARY KEY AUTO_INCREMENT,
  name varchar(255) UNIQUE NOT NULL,
  headquarters varchar(255),
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
