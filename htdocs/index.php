<?php

include_once(__DIR__ . "/../lib/PHAS.php");

$logfile = __DIR__ . "/../phas.log";
$database = array (
	"DSN" => "sqlite:" . __DIR__ . "/../main.sqlite"
);

$phas = new PHAS();
$phas->setOutputHandler('cv', 'cv_output');
$phas->setOutputHandler('xml', 'xml_otuput', 'text/xml; charset=utf8');
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

function xml_otuput( $data ) {
    if (is_numeric($data)) $data = array('id' => $data);
    return  toXml($data, "resp");
}

function toXml($data, $rootNodeName = 'data', $xml=null) {
    if ($xml == null) {
        $xml = simplexml_load_string("<?xml version='1.0' encoding='utf-8'?><$rootNodeName />");
        if (is_string($data) && substr($data, 0, 3) == "COD" ) {
            $code = substr($data, 4);
        } else {
            $code = "200";
        }
        $xml->addAttribute("code", $code);
    }

    if (is_array($data) and count($data)>0) {
        // loop through the data passed in.
        foreach($data as $key => $value) {
            if (is_array($value)) {
                list ($key, $foo) = explode("_", $key);

                // replace anything not alpha numeric
                $key = preg_replace('/[^a-z\-_]/i', '', $key);

                // if there is another array found recrusively call this function
                if (is_array($value)) {
                    $node = $xml->addChild($key);
                    // recrusive call.
                    toXml($value, $key, $node);
                } else {
                    // add single node.
                    $value = htmlentities($value);
                    $xml->addAttribute($key,$value);
                }
            }
        }
    }
    // pass back as string. or simple xml object if you want!
    return $xml->asXML();
}
