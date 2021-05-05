create table account(
email nvarchar (60) NOT NULL,
first_name nvarchar (20) NOT NULL,
last_name nvarchar (40) NOT NULL,
birthday char (6),
password nvarchar (30) NOT NULL,
PRIMARY KEY (email)
);


create table recipes(
recipeid int NOT NULL AUTO_INCREMENT,
title nvarchar (50) NOT NULL,
portion int NOT NULL,
ingredients text NOT NULL,
instructions text NOT NULL,
likes int NULL,
picture nvarchar(80) NOT NULL,
email nvarchar(60) NOT NULL,
PRIMARY KEY (recipeid),
FOREIGN KEY (email) REFERENCES account (email)
);


create table comments(
commentid int NOT NULL AUTO_INCREMENT,
recipeid int NOT NULL,
sentence nvarchar (100) NOT NULL,
PRIMARY KEY (commentid),
FOREIGN KEY (recipeid) REFERENCES recipes (recipeid)
);

