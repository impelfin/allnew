use testdb;

CREATE TABLE images (
  id int NOT NULL AUTO_INCREMENT,
  filename varchar(50) DEFAULT NULL,
  image_data longblob,
  PRIMARY KEY (id)
) 