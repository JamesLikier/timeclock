BEGIN;

DROP TABLE IF EXISTS employee;
CREATE TABLE employee (
    employeeid INTEGER PRIMARY KEY AUTOINCREMENT,
    username text UNIQUE,
    fname text,
    lname text,
    admin int DEFAULT 0
);

CREATE INDEX employee_username on employee (username);

DROP TABLE IF EXISTS punch;
CREATE TABLE punch (
    punchid INTEGER PRIMARY KEY AUTOINCREMENT,
    employeeid int REFERENCES employee (employeeid),
    punchdatetime text,
    createdbyemployeeid int REFERENCES employee (employeeid)
);

CREATE INDEX punch_employeeid_punchdatetime on punch (employeeid, punchdatetime DESC);

DROP TABLE IF EXISTS punch_correction_request;
CREATE TABLE punch_correction_request (
    pcrid INTEGER PRIMARY KEY AUTOINCREMENT,
    employeeid int REFERENCES employee (employeeid),
    punchdatetime text,
    approved int DEFAULT 0
);

CREATE INDEX pcr_employeeid_punchdatetime on punch_correction_request (employeeid, punchdatetime DESC);

INSERT INTO employee (username, fname, lname, admin) values ('admin','admin','admin',1);

COMMIT;