--Run this in local if you want to execute it
--GRANT ALL PRIVILEGES ON *.* TO 'username'@'localhost' IDENTIFIED BY 'password';
CREATE DATABASE scrapping;
USE scrapping;

CREATE TABLE companies (
  id int PRIMARY KEY AUTO_INCREMENT,
  name varchar(255) UNIQUE NOT NULL,
  headquarters varchar(255),
  rating float,
  rating_count int,
  benefits_rating float,
  benefits_rating_count int,
  size int,
  founded int,
  type varchar(255),
  website varchar(255),
  competitors varchar(255)
);

CREATE TABLE job_offers (
  id int PRIMARY KEY AUTO_INCREMENT,
  job_id int UNIQUE NOT NULL,
  city varchar(255),
  position varchar(255),
  description varchar(255),
  salary int,
  company_id int,
  FOREIGN KEY (company_id) REFERENCES companies (id)
);
