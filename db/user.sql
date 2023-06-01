use testdb;

CREATE TABLE user (
  userid char(8) NOT NULL,
  passwd char(8) DEFAULT NULL,
  PRIMARY KEY (userid)
);

insert into testdb.user values('moon', '1234');
insert into testdb.user values('admin', '1234');
insert into testdb.user values('root', '1234');

