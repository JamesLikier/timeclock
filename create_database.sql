BEGIN;

CREATE TABLE IF NOT EXISTS employee (
    employeeid INTEGER PRIMARY KEY AUTOINCREMENT,
    username text UNIQUE,
    fname text,
    lname text,
    admin int DEFAULT 0
);

CREATE INDEX IF NOT EXISTS employee_username on employee (username);

CREATE TABLE IF NOT EXISTS punch (
    punchid INTEGER PRIMARY KEY AUTOINCREMENT,
    employeeid int REFERENCES employee (employeeid),
    punchdatetime text,
    createdbyemployeeid int REFERENCES employee (employeeid)
);

CREATE INDEX IF NOT EXISTS punch_employeeid_punchdatetime on punch (employeeid, punchdatetime DESC);

CREATE TABLE IF NOT EXISTS punch_correction_request (
    pcrid INTEGER PRIMARY KEY AUTOINCREMENT,
    employeeid int REFERENCES employee (employeeid),
    punchdatetime text,
    approved int DEFAULT 0
);

CREATE INDEX IF NOT EXISTS pcr_employeeid_punchdatetime on punch_correction_request (employeeid, punchdatetime DESC);

CREATE TABLE IF NOT EXISTS auth (
    employeeid INTEGER PRIMARY KEY,
    password BLOB,
    FOREIGN KEY (employeeid) REFERENCES employee (employeeid)
);

INSERT OR IGNORE INTO employee (username, fname, lname, admin) values ('admin','admin','admin',1);

COMMIT;