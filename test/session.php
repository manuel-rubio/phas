<?php

chdir(__DIR__);

include_once(__DIR__ . "/../lib/PHAS.php");

$logfile = __DIR__ . "/../phas.log";
$database = array (
        "DSN" => "sqlite:/tmp/main.sqlite"
);

DataAccess::setDB(array ( "main" => $database ));
$main = DataAccess::singleton("main");

$data = $main->dql("SELECT * FROM phas_modules WHERE name = 'test'");
if (is_array($data) and count($data) == 0) {
    $main->dml("INSERT INTO phas_modules(name) VALUES (?)", array ( array ( 'test' ) ) );
}

$script = <<<EOF
session.data = [ 1, 2, 3 ]
"session guardada";
EOF;

$main->dml("DELETE FROM phas_codeversions WHERE code_id = (SELECT id FROM phas_codes WHERE name = 'sess_put')");
$main->dml("DELETE FROM phas_codes WHERE name = 'sess_put'");
$main->dml("INSERT INTO phas_codes( name, module_id, created_at, updated_at ) VALUES ( ?, ?, ?, ? )", array ( array ( 'sess_put', 1, date('Y-m-d H:i:s'), date('Y-m-d H:i:s') ) ) );
$main->dml("INSERT INTO phas_codeversions( content, version, code_id ) VALUES ( ?, ?, (SELECT id FROM phas_codes WHERE name = ? ) )", array ( array ( $script, 1, 'sess_put' ) ) );

$script = <<<EOF
[session.session_id(), session.data]
EOF;

$main->dml("DELETE FROM phas_codeversions WHERE code_id = (SELECT id FROM phas_codes WHERE name = 'sess_get')");
$main->dml("DELETE FROM phas_codes WHERE name = 'sess_get'");
$main->dml("INSERT INTO phas_codes( name, module_id, created_at, updated_at ) VALUES ( ?, ?, ?, ? )", array ( array ( 'sess_get', 1, date('Y-m-d H:i:s'), date('Y-m-d H:i:s') ) ) );
$main->dml("INSERT INTO phas_codeversions( content, version, code_id ) VALUES ( ?, ?, (SELECT id FROM phas_codes WHERE name = ? ) )", array ( array ( $script, 1, 'sess_get' ) ) );
