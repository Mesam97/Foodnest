
create table recipes(
recipeid int primary key NOT NULL IDENTITY(1,1),
title nvarchar (50) NOT NULL,
portion int NOT NULL,
ingredients nvarchar (200) NOT NULL,
instructions nvarchar (400) NOT NULL,
likes int NULL,
picture nvarchar(80) NOT NULL
);

go
create table comments(
commentid int primary key NOT NULL IDENTITY(1,1),
receptid int NOT NULL,
sentence nvarchar (100) NOT NULL
FOREIGN KEY (receptid) REFERENCES recipes (recipeid)
);