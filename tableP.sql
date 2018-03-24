CREATE TABLE P (
	id BIGINT AUTO_INCREMENT NOT NULL primary key,
	fullurl VARCHAR(60),
	pastedate VARCHAR(30),
	pastekey VARCHAR(30),
	size BIGINT,
	expire INT,
	title VARCHAR(128),
	syntax VARCHAR(30),
	user VARCHAR(128),
	txt LONGTEXT,
	UNIQUE(fullurl, pastedate, pastekey, size, expire, title, syntax, user)
);

