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
var http = new HTTP('http://project.bosqueviejo.net/erldev/browser/trunk/vsn.mk');
http.addQueryData('format', 'txt');
http.send();

[http.getCode(), http.getBody()];
EOF;

$data = $main->dql("SELECT * FROM phas_groups");
if (is_array($data) and count($data) == 0) {
    $main->dml("INSERT INTO phas_groups(name) VALUES (?)", array ( array ( 'test' ) ) );
}

$main->dml("DELETE FROM phas_phas WHERE module = 'vsn'");
$main->dml("INSERT INTO phas_phas( module, code, version, group_id, created_at ) VALUES ( ?, ?, ?, ?, ? )", array ( array ( 'vsn', $script, 0, 1, date('Y-m-d H:i:s') ) ) );
