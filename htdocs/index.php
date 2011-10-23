<?php

header("Content-type: text/plain");

include_once(__DIR__ . "/../lib/PHAS.php");
include_once(__DIR__ . "/../conf/config.php");

if (!isset($_REQUEST['module'])) {
    throw new Exception("ERROR: debe indicar un modulo.");
}

if ($env == "auto" or $env == "") {
    if (ini_get("dev_server")) {
        $env = "dev";
    } elseif (ini_get("prepro_server")) {
        $env = "prepro";
    } else {
        $env = "prod";
    }
}

if (isset($_REQUEST['env_especial'])) {
    $env = $env_especial;
}

include_once(__DIR__ . "/../conf/$env/config.php");
include_once(__DIR__ . "/../conf/$env/databases.php");

$log = Log::factory('file', $logfile, 'PHAS');

if (!isset($databases['main'])) {
    throw new Exception("ERROR: entorno [$env] no valido.");
} 

$db_main = $databases['main'];
unset($databases['main']);

DataAccess::setDB(array ( "main" => $db_main ));
$module = $_REQUEST['module'];
$main = new DataAccess("main");
$res = $main->dql("SELECT code FROM phas_phas WHERE module = ?", array ( $module ));

if ((is_array($res) and count($res) == 0) or !is_array($res)) {
    throw new Exception("ERROR: modulo [$module] no encontrado");
}

DataAccess::setDB($databases);
$js = new JS($log, session_id());
print $js->evaluateScript($res[0]["code"]);

