<?php

include_once("Log.php");
include_once(__DIR__ . "/PHAS/JS.php");
include_once(__DIR__ . "/PHAS/SoapCli.php");
include_once(__DIR__ . "/PHAS/DataAccess.php");
include_once(__DIR__ . "/PHAS/Session.php");
include_once(__DIR__ . "/PHAS/Request.php");
include_once(__DIR__ . "/PHAS/HTTP.php");

function console( $data ) {
	return print_r($data, true);
}

function exception_error_handler($errno, $errstr, $errfile, $errline ) {
    throw new ErrorException($errstr, 0, $errno, $errfile, $errline);
}
set_error_handler("exception_error_handler", E_USER_ERROR);

class PHAS {
	
	private $request;
	private $main;
	
	public function __construct() {
		global $log, $logfile, $database;
		$this->request = new Request();
		
		if (isset($logfile)) {
			$log = Log::factory('file', $logfile, 'PHAS');
		} else {
			$log = Log::factory('console', null, 'PHAS');
		}

		if (!isset($database['DSN'])) {
		    $msg = "ERROR: entorno [$env] no valido.";
		    $log->log($msg, PEAR_LOG_CRIT);
		    print $msg; die;
		} 
		DataAccess::setDB(array ( "main" => $database ));
		$this->main = DataAccess::singleton('main');
	}

	public function run() {
		if (!isset($this->request->module)) {
			print "Module not defined.";
			return;
		}
		$code = $this->checkModule();
		$serializer = $this->checkOutput();
		$this->configureDB();
		return $this->evaluate($code, $serializer);
	}
	
	private function checkOutput() {
		if (isset($this->request->output)) {
			switch ($this->request->output) {
			    case "PHP":
			    case "php":
			        $serializer = 'serialize';
					header("Content-type: text/plain");
			        break;
			    case "TXT":
			    case "txt":
				case "text":
				case "TEXT":
					$serializer = 'console';
					header("Content-type: text/plain");
					break;
			    case "JSON":
			    case "json":
			    default:
			        $serializer = 'json_encode';
					header("Content-type: text/plain");
			}
		} else {
	        $serializer = 'json_encode';
			header("Content-type: text/plain");
		}
		return $serializer;
	}

	private function evaluate( $code, $serializer ) {
		global $log;
		$js = new JS($log, session_id());
		$data = $js->evaluateScript($code);
		return $serializer($this->cleanup($data));
	}
	
	private function checkModule() {
		$module = $this->request->module;
		$res = $this->main->dql("
			SELECT code 
			FROM phas_phas 
			WHERE module = ? 
			ORDER BY version DESC
		", array ( $module ));

		if ((is_array($res) and count($res) == 0) or !is_array($res)) {
		    $msg = "ERROR: modulo [$module] no encontrado";
		    $log->log($msg, PEAR_LOG_CRIT);
		    print $msg; die;
		}
		return $res[0]["code"];
	}

	private function configureDB() {
		$databases_raw = $this->main->dql("
			SELECT *
			FROM phas_basesdedatos
		");
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
