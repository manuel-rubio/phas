<?php

header("Content-type: text/plain");

include_once(__DIR__ . "/../lib/PHAS.php");
include_once(__DIR__ . "/../conf/config.php");

if (!isset($_REQUEST['module'])) {
    print "ERROR: debe indicar un modulo."; die;
}

$serializer = 'json_encode';
switch ($_REQUEST['output']) {
    case "PHP":
    case "php":
        $serializer = 'serialize';
        break;
    case "JSON":
    case "json":
    default:
        $serializer = 'json_encode';
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
    $msg = "ERROR: entorno [$env] no valido.";
    $log->log($msg, PEAR_LOG_CRIT);
    print $msg; die;
} 

$db_main = $databases['main'];
unset($databases['main']);

DataAccess::setDB(array ( "main" => $db_main ));
$module = $_REQUEST['module'];
$main = new DataAccess("main");
$res = $main->dql("SELECT code FROM phas_phas WHERE module = ? ORDER BY version DESC", array ( $module ));

if ((is_array($res) and count($res) == 0) or !is_array($res)) {
    $msg = "ERROR: modulo [$module] no encontrado";
    $log->log($msg, PEAR_LOG_CRIT);
    print $msg; die;
}

DataAccess::setDB($databases);
$js = new JS($log, session_id());
$data = $js->evaluateScript($res[0]["code"]);
print $serializer(cleanup($data));

function cleanup( $data ) {
    $p = array();
    if (is_object($data) or is_array($data)) {
        foreach ($data as $k => $v) {
            $p[$k] = cleanup($v);
        }
    } else {
        $p = $data;
    }
    return $p;
}

