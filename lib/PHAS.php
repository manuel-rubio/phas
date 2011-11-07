<?php

include_once("Log.php");
include_once(__DIR__ . "/PHAS/JS.php");
include_once(__DIR__ . "/PHAS/SoapCli.php");
include_once(__DIR__ . "/PHAS/DataAccess.php");
include_once(__DIR__ . "/PHAS/Session.php");
include_once(__DIR__ . "/PHAS/Request.php");
include_once(__DIR__ . "/PHAS/HTTP.php");
include_once(__DIR__ . "/PHAS/Backend.php");
include_once(__DIR__ . "/PHAS/WSDLGenerator.php");
include_once(__DIR__ . "/PHAS/SoapGenerator.php");

define("PHAS_VERSION", "1.0");

function exception_error_handler($errno, $errstr, $errfile, $errline ) {
	throw new ErrorException($errstr, 0, $errno, $errfile, $errline);
}
set_error_handler("exception_error_handler", E_USER_ERROR);

ini_set("session.use_cookies",0);
ini_set("session.use_only_cookies",0);
header("X-Powered-By: PHAS-JS/" . PHAS_VERSION);

class PHAS {

	private $request;
	private $main;
	private $output_handlers;

	public function __construct() {
	    global $log, $logfile, $database;
	    $this->request = new Request();

	    if (isset($logfile)) {
	        $log = Log::factory('file', $logfile, 'PHAS');
	    } else {
	        $log = Log::factory('console', null, 'PHAS');
	    }

	    if (!isset($database['DSN'])) {
	        $msg = 'ERROR: $database not defined.';
	        $log->log($msg, PEAR_LOG_CRIT);
	        print $msg; die;
	    }
		$this->main = Backend::factory();
	    $this->output_handlers = array (
	        'txt' => array (
	            'function' => 'console',
	            'type' => 'text/plain'
	        ),
	        'php' => array (
	            'function' => 'serialize',
	            'type' => 'text/plain'
	        ),
			'xml' => array (
				'function' => 'xml_serialize',
				'type' => 'text/xml; charset=utf8'
			),
	    );
		if (function_exists('yaml_emit')) {
			$this->output_handlers['yaml'] = array (
				'function' => 'yaml_emit',
				'type' => 'text/plain'
			);
		}
		if (function_exists('json_encode')) {
	        $this->output_handlers['json'] = array (
	            'function' => 'json_encode',
	            'type' => 'application/json'
	        );
		}
	    $this->session_handler = 'PHPSession';
	}

	public function run() {
	    if (!isset($this->request->group)) {
	        print "Group not defined.";
	        return;
	    }
	    if (isset($this->request->wsdl)) {
            header("Content-type: text/xml; charset=utf8");
            $wsdl = new WSDLGenerator($this->main);
            print $wsdl->generate($this->request->group);
            return;
	    }
	    if (isset($this->request->soap)) {
            $wsdl = new WSDLGenerator($this->main);
            $soap = new SoapGenerator($this->request->group, $wsdl, $this->main);
            $this->configureDB();
            $soap->handle($this->session_handler);
            return;
	    }
        if (!isset($this->request->module)) {
            print "Module not defined.";
            return;
        }
	    $code = $this->checkModule();
	    $serializer = $this->checkOutput();
	    $this->configureDB();
	    return $this->evaluate($code, $serializer);
	}

	public function setOutputHandler( $name, $function, $type = 'text/plain' ) {
	    $this->output_handlers[$name] = array (
	        'function' => $function,
	        'type' => $type
	    );
	}

	public function setSessionHandler( $class ) {
	    $this->session_handler = $class;
	}

	private function checkOutput() {
	    if (isset($this->request->output)) {
	        $output = $this->request->output;
	    } else {
	        $output = 'php';
	    }
	    if (isset($this->output_handlers[$output])) {
	        $output = $this->output_handlers[$output];
	    } else {
	        $output = $this->output_handlers['php'];
	    }
	    header("Content-type: {$output['type']}");
	    return $output['function'];
	}

	private function evaluate( $code, $serializer ) {
	    global $log;
	    $sid = $this->request->SID;
	    $session = Session::factory($this->session_handler, $sid);
	    header("X-Session: " . $session->session_id());
	    $js = new JS($log, $session);
	    $data = $js->evaluateScript($code);
	    return $serializer($this->cleanup($data));
	}

	private function checkModule() {
	    global $log;
	    $module = $this->request->module;
	    $group = $this->request->group;
	    $res = $this->main->getCode($module, $group);

	    if ((is_array($res) and count($res) == 0) or !is_array($res)) {
	        $msg = "ERROR: modulo [$module] del grupo [$group] no encontrado";
	        $log->log($msg, PEAR_LOG_CRIT);
	        print $msg; die;
	    }
	    return $res[0]["code"];
	}

	public function configureDB() {
	    $databases_raw = $this->main->getDB();
	    $databases = array();
	    if (is_array($databases_raw) and count($databases_raw)>0) {
	        foreach ($databases_raw as $db) {
	            $databases[$db['name']] = array (
	                'DSN' => $db['DSN'],
	                'USR' => $db['USR'],
	                'PWD' => $db['PWD']
	            );
	        }
	    }
	    DataAccess::setDB($databases);
	    return $databases;
	}

	private function cleanup( $data ) {
	    $p = array();
	    if (is_object($data) or is_array($data)) {
	        foreach ($data as $k => $v) {
	            $p[$k] = $this->cleanup($v);
	        }
	    } else {
	        $p = $data;
	    }
	    return $p;
	}

}

function console( $data ) {
	return print_r($data, true);
}

function xml_serialize( $data ) {
	global $xml_options;
	if (!$xml_options) {
		$xml_options = array (
			'defaultTagName' => 'data',
			'rootName' => 'resp',
			'encoding' => 'utf8',
			'scalarAsAttributes' => true,
		);
	}
	include("XML/Serializer.php");
	$serializer = new XML_Serializer($xml_options);
	$serializer->serialize($data);
	return $serializer->getSerializedData();
}
