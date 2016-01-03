CREATE TABLE family (
	bid TINYINT NOT NULL PRIMARY KEY,
	name VARCHAR(30) NOT NULL
);

CREATE TABLE sdk_release_dates (
	sdk_version TINYINT NOT NULL PRIMARY KEY,
	date_release INTEGER NOT NULL
);

CREATE TABLE samples (
	bid TINYINT NOT NULL,
	md5 VARCHAR(32) NOT NULL,
	sha1 VARCHAR(40) NOT NULL,
	sha256 VARCHAR(64) NOT NULL,
	stype VARCHAR(10),
	fingerprint VARCHAR(32),
	package_name VARCHAR(256),
	min_sdk TINYINT,
	max_sdk TINYINT,
	date_zip_modified INTEGER,
	date_release INTEGER,
	date_virustotal INTEGER,
	date_andrubis INTEGER,
	andrubis_taskid VARCHAR(33),
	PRIMARY KEY (md5, sha1, sha256)
);

CREATE TABLE fingerprints (
	fingerprint VARCHAR(32) PRIMARY KEY,
	name VARCHAR(256) NOT NULL
);
