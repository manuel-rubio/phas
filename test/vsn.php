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

$data = $main->dql("SELECT * FROM phas_modules WHERE name = 'test'");
if (is_array($data) and count($data) == 0) {
    $main->dml("INSERT INTO phas_modules(name) VALUES (?)", array ( array ( 'test' ) ) );
}

$main->dml("DELETE FROM phas_codeversions WHERE code_id = (SELECT id FROM phas_codes WHERE name = 'vsn')");
$main->dml("DELETE FROM phas_codes WHERE name = 'vsn'");
$main->dml("INSERT INTO phas_codes( name, module_id, version, created_at, updated_at ) VALUES ( ?, ( SELECT id FROM phas_modules WHERE name = ? ), ?, ?, ? )", array ( array ( 'vsn', 'test', 1, date('Y-m-d H:i:s'), date('Y-m-d H:i:s') ) ) );
$main->dml("INSERT INTO phas_codeversions( content, version, code_id ) VALUES ( ?, ?, (SELECT id FROM phas_codes WHERE name = 'vsn' ) )", array ( array ( $script, 1 ) ) );

