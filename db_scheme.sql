/*
 Date: 10/10/2022 00:42:54
*/

PRAGMA foreign_keys = false;

-- ----------------------------
-- Table structure for connections
-- ----------------------------
DROP TABLE IF EXISTS "connections";
CREATE TABLE connections (user_id INT REFERENCES users (user_id) NOT NULL, exception_id INT REFERENCES exceptions (exception_id) NOT NULL, connection_creating_date DATETIME);

-- ----------------------------
-- Table structure for e_additions
-- ----------------------------
DROP TABLE IF EXISTS "e_additions";
CREATE TABLE "e_additions" (
  "e_number" STRING NOT NULL,
  "e_name" STRING,
  "harm" STRING,
  "property" STRING,
  "usage" STRING,
  "influence" STRING,
  PRIMARY KEY ("e_number")
);

-- ----------------------------
-- Table structure for exceptions
-- ----------------------------
DROP TABLE IF EXISTS "exceptions";
CREATE TABLE exceptions (exception_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, exception_name STRING);

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS "users";
CREATE TABLE users (user_id INTEGER NOT NULL UNIQUE PRIMARY KEY AUTOINCREMENT, user_name STRING, user_creating_date DATETIME);

PRAGMA foreign_keys = true;
