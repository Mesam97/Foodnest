create table account(
email nvarchar (60) primary key NOT NULL,
first_name nvarchar (20) NOT NULL,
last_name nvarchar (40) NOT NULL,
birthday char (6),
password nvarchar (30) NOT NULL
);

GO
create table recipes(
recipeid int primary key NOT NULL IDENTITY(1,1),
title nvarchar (50) NOT NULL,
portion int NOT NULL,
ingredients nvarchar (200) NOT NULL,
instructions nvarchar (400) NOT NULL,
likes int NULL,
picture nvarchar(80) NOT NULL
);

GO
create table comments(
commentid int primary key NOT NULL IDENTITY(1,1),
receptid int NOT NULL,
sentence nvarchar (100) NOT NULL
FOREIGN KEY (receptid) REFERENCES recipes (recipeid)
);