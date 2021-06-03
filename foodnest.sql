CREATE DATABASE Foodnest;

CREATE TABLE Account(
Email VARCHAR (60) NOT NULL,
First_name VARCHAR (20) NOT NULL,
Last_name VARCHAR (40) NOT NULL,
Birthday CHAR (6),
Password BLOB NOT NULL,
PRIMARY KEY (Email)
);


CREATE TABLE Recipes(
Recipeid INT NOT NULL AUTO_INCREMENT,
Title VARCHAR (50) NOT NULL,
Portion INT NOT NULL,
Ingredients TEXT NOT NULL,
Instructions TEXT NOT NULL,
Picture VARCHAR (80) NOT NULL,
Email VARCHAR (60) NOT NULL,
Categories TEXT NULL,
PRIMARY KEY (Recipeid),
FOREIGN KEY (Email) REFERENCES Account (Email)
);

CREATE TABLE Comments(
Commentid INT NOT NULL AUTO_INCREMENT,
Recipeid INT NOT NULL,
Sentence VARCHAR (100) NOT NULL,
Email Varchar (60) NOT NULL,
PRIMARY KEY (Commentid),
FOREIGN KEY (Recipeid) REFERENCES Recipes (Recipeid),
FOREIGN KEY (Email) REFERENCES Account (Email)
);

CREATE TABLE Likes(
Recipeid INT,
Email VARCHAR (60),
PRIMARY KEY (Recipeid, Email),
FOREIGN KEY (Email) REFERENCES Account (Email),
FOREIGN KEY (Recipeid) REFERENCES Recipes (Recipeid)
);

CREATE TABLE Tags(
Tagid int NOT NULL AUTO_INCREMENT,
Categories TEXT NULL,
Recipeid INT NOT NULL,
PRIMARY KEY (Tagid),
FOREIGN KEY (Recipeid) REFERENCES Recipes(Recipeid)
);