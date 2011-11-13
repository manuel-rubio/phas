<?php

include_once("Log.php");
include_once(__DIR__ . "/PHAS/JS.php");
include_once(__DIR__ . "/PHAS/SoapCli.php");
include_once(__DIR__ . "/PHAS/Cache.php");
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
	private $cache;

	public function __construct() {
	    global $log, $logfile, $database, $cache;
	    $this->request = new Request();
		$this->cache = Cache::factory($cache);

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
		global $log;
	    if (!isset($this->request->module)) {
	        return "Module not defined.";
	    }
	    if (isset($this->request->wsdl)) {
            header("Content-type: text/xml; charset=utf8");
			$key = 'wsdl/' . $this->request->module;
			if ($this->cache and isset($this->request->cache)) {
				$data = $this->cache->get($key, $succ);
				if ($succ) {
					$log->log("Hit: $key", PEAR_LOG_INFO);
					return $data;
				}
			}
            $wsdl = new WSDLGenerator($this->main);
            $data = $wsdl->generate($this->request->module);
			if ($this->cache and isset($this->request->cache)) {
				$this->cache->set($key, $data);
			}
            return $data;
	    }
	    if (isset($this->request->soap)) {
			$key = 'soap/' . $this->request->module . '/' . md5(http_get_request_body());
			if ($this->cache and isset($this->request->cache)) {
				$data = $this->cache->get($key, $succ);
				if ($succ) {
					return $data;
				}
			}
            $wsdl = new WSDLGenerator($this->main);
            $soap = new SoapGenerator($this->request->module, $wsdl, $this->main);
            $this->configureDB();
            $response = $soap->handle($this->session_handler);
			if ($this->cache and isset($this->request->cache)) {
				$this->cache->set($key, $response);
			}
			$log->log("Response SOAP: $response", PEAR_LOG_DEBUG);
            return $response;
	    }
        if (!isset($this->request->code)) {
            return "Code not defined.";
        }
		$key = 'call/' . $this->request->module . '/' . $this->request->code . '/' . $this->request->output;
		if ($this->cache and isset($this->request->cache)) {
			$data = $this->cache->get($key, $succ);
			if ($succ) {
				header("Content-type: {$data['content-type']}");
				return $data['resp'];
			}
		}
	    $code = $this->checkCode();
	    $serializer = $this->checkOutput();
	    $this->configureDB();
	    $response = $this->evaluate($code, $serializer);
		if ($this->cache and isset($this->request->cache)) {
			$this->cache->set($key, array (
				'resp' => $response,
				'content-type' => $this->getOutputType()
			));
		}
		return $response;
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
	
	private function getOutputType() {
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
	    return $output['type'];
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

	private function checkCode() {
	    global $log;
	    $code = $this->request->code;
	    $module = $this->request->module;
	    $res = $this->main->getCode($code, $module);

	    if ((is_array($res) and count($res) == 0) or !is_array($res)) {
	        $msg = "ERROR: modulo [$code] del grupo [$module] no encontrado";
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
