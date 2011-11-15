BEGIN;
CREATE TABLE `phas_modules` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `name` varchar(50) NOT NULL
)
;
CREATE TABLE `phas_codes` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `name` varchar(50) NOT NULL,
    `module_id` integer NOT NULL,
    `version` integer NOT NULL,
    `doc` longtext NOT NULL,
    `created_at` datetime NOT NULL,
    `updated_at` datetime NOT NULL
)
;
ALTER TABLE `phas_codes` ADD CONSTRAINT `module_id_refs_id_153f8434` FOREIGN KEY (`module_id`) REFERENCES `phas_modules` (`id`);
CREATE TABLE `phas_codeversions` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `content` longtext NOT NULL,
    `version` integer NOT NULL,
    `return_attr_id` integer,
    `code_id` integer NOT NULL
)
;
ALTER TABLE `phas_codeversions` ADD CONSTRAINT `code_id_refs_id_eaeb02c6` FOREIGN KEY (`code_id`) REFERENCES `phas_codes` (`id`);
CREATE TABLE `phas_codeattrs` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `name` varchar(50) NOT NULL,
    `tad_id` integer NOT NULL,
    `code_id` integer NOT NULL
)
;
ALTER TABLE `phas_codeattrs` ADD CONSTRAINT `code_id_refs_id_b86f8359` FOREIGN KEY (`code_id`) REFERENCES `phas_codeversions` (`id`);
CREATE TABLE `phas_tad` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `name` varchar(50) NOT NULL,
    `xsd_name` varchar(50) NOT NULL,
    `tad_type` varchar(1) NOT NULL
)
;
ALTER TABLE `phas_codeversions` ADD CONSTRAINT `return_attr_id_refs_id_af9f13a7` FOREIGN KEY (`return_attr_id`) REFERENCES `phas_tad` (`id`);
ALTER TABLE `phas_codeattrs` ADD CONSTRAINT `tad_id_refs_id_9c3f2699` FOREIGN KEY (`tad_id`) REFERENCES `phas_tad` (`id`);
CREATE TABLE `phas_tadattrs` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `name` varchar(50) NOT NULL,
    `tad_id` integer NOT NULL,
    `tad_type_id` integer NOT NULL,
    `min_occurs` integer NOT NULL,
    `max_occurs` integer NOT NULL
)
;
ALTER TABLE `phas_tadattrs` ADD CONSTRAINT `tad_id_refs_id_4f66c06e` FOREIGN KEY (`tad_id`) REFERENCES `phas_tad` (`id`);
ALTER TABLE `phas_tadattrs` ADD CONSTRAINT `tad_type_id_refs_id_4f66c06e` FOREIGN KEY (`tad_type_id`) REFERENCES `phas_tad` (`id`);
CREATE TABLE `phas_databases` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `name` varchar(50) NOT NULL UNIQUE,
    `DSN` varchar(256) NOT NULL,
    `USR` varchar(50),
    `PWD` varchar(50)
)
;
CREATE INDEX `phas_codes_f53ed95e` ON `phas_codes` (`module_id`);
CREATE INDEX `phas_codeversions_aab20eb7` ON `phas_codeversions` (`return_attr_id`);
CREATE INDEX `phas_codeversions_476c40cb` ON `phas_codeversions` (`code_id`);
CREATE INDEX `phas_codeattrs_1d3a455c` ON `phas_codeattrs` (`tad_id`);
CREATE INDEX `phas_codeattrs_476c40cb` ON `phas_codeattrs` (`code_id`);
CREATE INDEX `phas_tadattrs_1d3a455c` ON `phas_tadattrs` (`tad_id`);
CREATE INDEX `phas_tadattrs_a5373f22` ON `phas_tadattrs` (`tad_type_id`);
COMMIT;

