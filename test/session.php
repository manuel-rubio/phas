<?php

chdir(__DIR__);

include_once(__DIR__ . "/../lib/PHAS.php");

$logfile = __DIR__ . "/../phas.log";
$database = array (
        "DSN" => "sqlite:/tmp/main.sqlite"
);

DataAccess::setDB(array ( "main" => $database ));
$main = DataAccess::singleton("main");

$script = <<<EOF
session.data = [ 1, 2, 3 ]
"session guardada";
EOF;

$main->dml("DELETE FROM phas_phas WHERE module = 'sess_put'");
$main->dml("INSERT INTO phas_phas( module, code, version, created_at ) VALUES ( ?, ?, ?, ? )", array ( array ( 'sess_put', $script, 0, date('Y-m-d H:i:s') ) ) );

$script = <<<EOF
[session.session_id(), session.data]
EOF;

$main->dml("DELETE FROM phas_phas WHERE module = 'sess_get'");
$main->dml("INSERT INTO phas_phas( module, code, version, created_at ) VALUES ( ?, ?, ?, ? )", array ( array ( 'sess_get', $script, 0, date('Y-m-d H:i:s') ) ) );

