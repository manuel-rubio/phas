BEGIN;
CREATE TABLE "phas_modules" (
    "id" serial NOT NULL PRIMARY KEY,
    "name" varchar(50) NOT NULL
)
;
CREATE TABLE "phas_codes" (
    "id" serial NOT NULL PRIMARY KEY,
    "name" varchar(50) NOT NULL,
    "module_id" integer NOT NULL REFERENCES "phas_modules" ("id") DEFERRABLE INITIALLY DEFERRED,
    "version" integer NOT NULL,
    "doc" text NOT NULL,
    "created_at" timestamp with time zone NOT NULL,
    "updated_at" timestamp with time zone NOT NULL
)
;
CREATE TABLE "phas_codeversions" (
    "id" serial NOT NULL PRIMARY KEY,
    "content" text NOT NULL,
    "version" integer NOT NULL,
    "return_attr_id" integer,
    "code_id" integer NOT NULL REFERENCES "phas_codes" ("id") DEFERRABLE INITIALLY DEFERRED
)
;
CREATE TABLE "phas_codeattrs" (
    "id" serial NOT NULL PRIMARY KEY,
    "name" varchar(50) NOT NULL,
    "tad_id" integer NOT NULL,
    "code_id" integer NOT NULL REFERENCES "phas_codeversions" ("id") DEFERRABLE INITIALLY DEFERRED
)
;
CREATE TABLE "phas_tad" (
    "id" serial NOT NULL PRIMARY KEY,
    "name" varchar(50) NOT NULL,
    "xsd_name" varchar(50) NOT NULL,
    "tad_type" varchar(1) NOT NULL
)
;
ALTER TABLE "phas_codeversions" ADD CONSTRAINT "return_attr_id_refs_id_af9f13a7" FOREIGN KEY ("return_attr_id") REFERENCES "phas_tad" ("id") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "phas_codeattrs" ADD CONSTRAINT "tad_id_refs_id_9c3f2699" FOREIGN KEY ("tad_id") REFERENCES "phas_tad" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE TABLE "phas_tadattrs" (
    "id" serial NOT NULL PRIMARY KEY,
    "name" varchar(50) NOT NULL,
    "tad_id" integer NOT NULL REFERENCES "phas_tad" ("id") DEFERRABLE INITIALLY DEFERRED,
    "tad_type_id" integer NOT NULL REFERENCES "phas_tad" ("id") DEFERRABLE INITIALLY DEFERRED,
    "min_occurs" integer NOT NULL,
    "max_occurs" integer NOT NULL
)
;
CREATE TABLE "phas_databases" (
    "id" serial NOT NULL PRIMARY KEY,
    "name" varchar(50) NOT NULL UNIQUE,
    "DSN" varchar(256) NOT NULL,
    "USR" varchar(50),
    "PWD" varchar(50)
)
;
CREATE INDEX "phas_codes_module_id" ON "phas_codes" ("module_id");
CREATE INDEX "phas_codeversions_return_attr_id" ON "phas_codeversions" ("return_attr_id");
CREATE INDEX "phas_codeversions_code_id" ON "phas_codeversions" ("code_id");
CREATE INDEX "phas_codeattrs_tad_id" ON "phas_codeattrs" ("tad_id");
CREATE INDEX "phas_codeattrs_code_id" ON "phas_codeattrs" ("code_id");
CREATE INDEX "phas_tadattrs_tad_id" ON "phas_tadattrs" ("tad_id");
CREATE INDEX "phas_tadattrs_tad_type_id" ON "phas_tadattrs" ("tad_type_id");
COMMIT;

