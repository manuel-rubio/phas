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
ALTER TABLE `phas_codeversions` ADD CONSTRAINT `code_id_refs_id_1514fd3a` FOREIGN KEY (`code_id`) REFERENCES `phas_codes` (`id`);
CREATE TABLE `phas_codeattrs` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `name` varchar(50) NOT NULL,
    `tad_id` integer,
    `code_id` integer
)
;
ALTER TABLE `phas_codeattrs` ADD CONSTRAINT `code_id_refs_id_47907ca7` FOREIGN KEY (`code_id`) REFERENCES `phas_codeversions` (`id`);
CREATE TABLE `phas_tad` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `name` varchar(50) NOT NULL,
    `complex` bool NOT NULL,
    `xsd_name` varchar(50) NOT NULL
)
;
ALTER TABLE `phas_codeversions` ADD CONSTRAINT `return_attr_id_refs_id_5060ec59` FOREIGN KEY (`return_attr_id`) REFERENCES `phas_tad` (`id`);
ALTER TABLE `phas_codeattrs` ADD CONSTRAINT `tad_id_refs_id_63c0d967` FOREIGN KEY (`tad_id`) REFERENCES `phas_tad` (`id`);
CREATE TABLE `phas_tadattrs` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `name` varchar(50) NOT NULL,
    `tad_id` integer
)
;
ALTER TABLE `phas_tadattrs` ADD CONSTRAINT `tad_id_refs_id_4f66c06e` FOREIGN KEY (`tad_id`) REFERENCES `phas_tad` (`id`);
CREATE TABLE `phas_databases` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `name` varchar(50) NOT NULL UNIQUE,
    `DSN` varchar(256) NOT NULL,
    `USR` varchar(50),
    `PWD` varchar(50)
)
;
CREATE INDEX `phas_codes_ac126a2` ON `phas_codes` (`module_id`);
CREATE INDEX `phas_codeversions_554df149` ON `phas_codeversions` (`return_attr_id`);
CREATE INDEX `phas_codeversions_476c40cb` ON `phas_codeversions` (`code_id`);
CREATE INDEX `phas_codeattrs_1d3a455c` ON `phas_codeattrs` (`tad_id`);
CREATE INDEX `phas_codeattrs_476c40cb` ON `phas_codeattrs` (`code_id`);
CREATE INDEX `phas_tadattrs_1d3a455c` ON `phas_tadattrs` (`tad_id`);
COMMIT;

