BEGIN;
CREATE TABLE "phas_modules" (
    "id" integer NOT NULL PRIMARY KEY,
    "name" varchar(50) NOT NULL
)
;
CREATE TABLE "phas_codes" (
    "id" integer NOT NULL PRIMARY KEY,
    "name" varchar(50) NOT NULL,
    "module_id" integer NOT NULL REFERENCES "phas_modules" ("id"),
    "version" integer NOT NULL,
    "doc" text NOT NULL,
    "created_at" datetime NOT NULL,
    "updated_at" datetime NOT NULL
)
;
CREATE TABLE "phas_codeversions" (
    "id" integer NOT NULL PRIMARY KEY,
    "content" text NOT NULL,
    "version" integer NOT NULL,
    "return_attr_id" integer,
    "code_id" integer NOT NULL REFERENCES "phas_codes" ("id")
)
;
CREATE TABLE "phas_codeattrs" (
    "id" integer NOT NULL PRIMARY KEY,
    "name" varchar(50) NOT NULL,
    "tad_id" integer,
    "code_id" integer REFERENCES "phas_codeversions" ("id")
)
;
CREATE TABLE "phas_tad" (
    "id" integer NOT NULL PRIMARY KEY,
    "name" varchar(50) NOT NULL,
    "complex" bool NOT NULL,
    "xsd_name" varchar(50) NOT NULL
)
;
CREATE TABLE "phas_tadattrs" (
    "id" integer NOT NULL PRIMARY KEY,
    "name" varchar(50) NOT NULL,
    "tad_id" integer REFERENCES "phas_tad" ("id")
)
;
CREATE TABLE "phas_databases" (
    "id" integer NOT NULL PRIMARY KEY,
    "name" varchar(50) NOT NULL UNIQUE,
    "DSN" varchar(256) NOT NULL,
    "USR" varchar(50),
    "PWD" varchar(50)
)
;
CREATE INDEX "phas_codes_ac126a2" ON "phas_codes" ("module_id");
CREATE INDEX "phas_codeversions_554df149" ON "phas_codeversions" ("return_attr_id");
CREATE INDEX "phas_codeversions_476c40cb" ON "phas_codeversions" ("code_id");
CREATE INDEX "phas_codeattrs_1d3a455c" ON "phas_codeattrs" ("tad_id");
CREATE INDEX "phas_codeattrs_476c40cb" ON "phas_codeattrs" ("code_id");
CREATE INDEX "phas_tadattrs_1d3a455c" ON "phas_tadattrs" ("tad_id");
COMMIT;

