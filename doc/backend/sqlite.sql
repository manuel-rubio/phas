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
    "tad_id" integer NOT NULL,
    "code_id" integer NOT NULL REFERENCES "phas_codeversions" ("id")
)
;
CREATE TABLE "phas_tad" (
    "id" integer NOT NULL PRIMARY KEY,
    "name" varchar(50) NOT NULL,
    "xsd_name" varchar(50) NOT NULL,
    "tad_type" varchar(1) NOT NULL
)
;
CREATE TABLE "phas_tadattrs" (
    "id" integer NOT NULL PRIMARY KEY,
    "name" varchar(50) NOT NULL,
    "tad_id" integer NOT NULL REFERENCES "phas_tad" ("id"),
    "tad_type_id" integer NOT NULL REFERENCES "phas_tad" ("id"),
    "min_occurs" integer NOT NULL,
    "max_occurs" integer NOT NULL
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
CREATE INDEX "phas_codes_f53ed95e" ON "phas_codes" ("module_id");
CREATE INDEX "phas_codeversions_aab20eb7" ON "phas_codeversions" ("return_attr_id");
CREATE INDEX "phas_codeversions_476c40cb" ON "phas_codeversions" ("code_id");
CREATE INDEX "phas_codeattrs_1d3a455c" ON "phas_codeattrs" ("tad_id");
CREATE INDEX "phas_codeattrs_476c40cb" ON "phas_codeattrs" ("code_id");
CREATE INDEX "phas_tadattrs_1d3a455c" ON "phas_tadattrs" ("tad_id");
CREATE INDEX "phas_tadattrs_a5373f22" ON "phas_tadattrs" ("tad_type_id");
COMMIT;

