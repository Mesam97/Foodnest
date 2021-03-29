create database foodnest;

create table Account(
email nvarchar (60) primary key NOT NULL,
f_name nvarchar (20) NOT NULL,
l_name nvarchar (40) NOT NULL,
b_day int,
password nvarchar (30) NOT NULL
);
create table Recept(
receptid int primary key NOT NULL IDENTITY(1,1),
title nvarchar (50) NOT NULL,
portion int NOT NULL,
ingresienses nvarchar (200) NOT NULL,
rec_desc nvarchar (400) NOT NULL;
likes int NULL
);
create table Comment(
commentid int primary key NOT NULL IDENTITY(1,1),
recept_id int NOT NULL,
sentence nverchar (100) NOT NULL
);

"""create table content(
contentid int primary key NOT NULL IDENTITY (1,1),
recept_id int NOT NULL,
ingrediens nvarchar (30) NOT NULL,
amount nvarchar (20) NOT NULL
);"""

