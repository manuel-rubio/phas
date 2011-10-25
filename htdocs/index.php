<?php

include_once(__DIR__ . "/../lib/PHAS.php");

$logfile = __DIR__ . "/../phas.log";
$database = array (
	"DSN" => "sqlite:" . __DIR__ . "/../main.sqlite"
);

$phas = new PHAS();
print $phas->run();
