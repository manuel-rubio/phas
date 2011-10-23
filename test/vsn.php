<?php

include_once(__DIR__ . "/../lib/PHAS.php");
include_once(__DIR__ . "/../conf/config.php");
include_once(__DIR__ . "/../conf/$env/config.php");
include_once(__DIR__ . "/../conf/$env/databases.php");

if (!isset($databases['main'])) {
    throw new Exception("ERROR: entorno [$env] no valido.");
} 

DataAccess::setDB($databases);
$main = new DataAccess("main");

$script = <<<EOF
var http = new HTTP('http://erldev.org/browser/trunk/vsn.mk');
http.addQueryData('format', 'txt');
http.send();

[http.getCode(), http.getBody()];
EOF;

$main->dml("DELETE FROM phas_phas WHERE module = 'vsn'");
$main->dml("INSERT INTO phas_phas( module, code, version, created_at ) VALUES ( ?, ?, ?, ? )", array ( array ( 'vsn', $script, 0, date('Y-m-d H:i:s') ) ) );

