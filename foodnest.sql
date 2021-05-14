CREATE DATABASE Foodnest;

CREATE TABLE Account(
Email NVARCHAR(60) NOT NULL,
First_name NVARCHAR(20) NOT NULL,
Last_name NVARCHAR(40) NOT NULL,
Birthday CHAR(6),
Password NVARCHAR(30) NOT NULL,
PRIMARY KEY (Email)
);


CREATE TABLE Recipes(
Recipeid INT NOT NULL AUTO_INCREMENT,
Title NVARCHAR(50) NOT NULL,
Portion INT NOT NULL,
Ingredients TEXT NOT NULL,
Instructions TEXT NOT NULL,
Likes INT NULL,
Picture NVARCHAR(80) NOT NULL,
Email NVARCHAR(60) NOT NULL,
PRIMARY KEY (recipeid),
FOREIGN KEY (Email) REFERENCES Account (Email)
);


CREATE TABLE Comments(
Commentid INT NOT NULL AUTO_INCREMENT,
Recipeid INT NOT NULL,
Sentence NVARCHAR(100) NOT NULL,
PRIMARY KEY (Commentid),
FOREIGN KEY (Recipeid) REFERENCES Recipes (Recipeid)
);

CREATE TABLE Post_likes(
Likeid INT AUTO_INCREMENT,
Recipeid INT,
Userid NVARCHAR(60), -- Email	
Liked BOOLEAN NOT NULL,
PRIMARY KEY(Likeid),
FOREIGN KEY(Userid) REFERENCES Account(Email),
FOREIGN KEY(Recipeid) REFERENCES Recipes(Recipeid)
);

CREATE TABLE Post_like_sum(
Recipeid INT,
Likes INT,
PRIMARY KEY(Recipeid),
FOREIGN KEY(Recipeid) REFERENCES Recipes(Recipeid)
);
