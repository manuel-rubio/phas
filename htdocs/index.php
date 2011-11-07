<?php

include_once(__DIR__ . "/../lib/PHAS.php");

$logfile = __DIR__ . "/../phas.log";
$database = array (
	"DSN" => "sqlite:/tmp/main.sqlite"
);

$phas = new PHAS();
$phas->setOutputHandler('cv', 'cv_output');
$phas->setOutputHandler('cbx', 'cbx_output', 'text/xml; charset=utf8');
print $phas->run();

function cbx_output( $data ) {
    return $data;
}

function cv_output( $data ) {
    $res =  "action_type=".$data['action']."\n";
    $res .=   "action_data=".$data['data']."\n";
    if (!empty($data['tts'])) {
        $res .=    "action_tts=".$data['tts']."\n";
    }
    if (!empty($data['additional_data'])) {
        $res .=    "additional_data=".urlencode($data['additional_data'])."\n";
    }
    if (!empty($data['session_id'])) {
        $res .=    "action_sesid=".$data['session_id']."\n";
    } else {
        $session_id = session_id();
        if (!empty($session_id)) {
            $res .= "action_sesid=" . session_id() . "\n";
        }
    }
    return $res;
}
