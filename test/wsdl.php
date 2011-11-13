<?php

chdir(__DIR__);

include_once(__DIR__ . "/../lib/PHAS.php");

$logfile = __DIR__ . "/../phas.log";
$database = array (
        "DSN" => "sqlite:/tmp/main.sqlite"
);

DataAccess::setDB(array ( "main" => $database ));
$main = DataAccess::singleton("main");

$main->dml("DELETE FROM phas_tad");
$main->dml("INSERT INTO phas_tad( name, complex, xsd_name ) VALUES ( ?, ?, ? )", array (
	array ( 'string', 0, 'xsd:string' ),
    array ( 'integer', 0, 'xsd:integer' ),
    array ( 'int', 0, 'xsd:integer' ),
    array ( 'boolean', 0, 'xsd:boolean' ),
    array ( 'bool', 0, 'xsd:boolean' ),
    array ( 'string[]', 0, 'tns:ArrayOfString' ),
    array ( 'string[][]', 0, 'tns:MatrixOfString' ),
));

$main->dml("UPDATE phas_codeversions SET return_attr_id = ? WHERE code_id = (SELECT id FROM phas_codes WHERE name = ? )", array(
    array ( 6, 'vsn' ),
));

$api = new SoapClient("http://localhost/~bombadil/phas/?module=test&wsdl");
print_r($api->vsn());
