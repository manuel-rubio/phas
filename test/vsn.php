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
var http = new HTTP('http://erldev.org/browser/trunk/vsn.mk');
http.addQueryData('format', 'txt');
http.send();

[http.getCode(), http.getBody()];
EOF;

$main->dml("DELETE FROM phas_phas WHERE module = 'vsn'");
$main->dml("INSERT INTO phas_phas( module, code, version, created_at ) VALUES ( ?, ?, ?, ? )", array ( array ( 'vsn', $script, 0, date('Y-m-d H:i:s') ) ) );

