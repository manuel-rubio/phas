<?php

class SoapGenerator {

    private $soap_server;
    private $main;

    public function __construct( $module, &$wsdl, &$main ) {
        global $wsdl_path, $wsdl_cache;
        $wsdl_cache = empty($wsdl_cache) ? 0 : $wsdl_cache;
        $wsdl_path = empty($wsdl_path) ? '/tmp' : $wsdl_path;
        $file = $wsdl_path . '/wsdl-api-' . $module;
        $f_cache = file_exists($file) ? stat($file) : array ( 'mtime' => 0 );
        if ($f_cache['mtime'] + $wsdl_cache < time()) {
            $this->cacheGen($module, $wsdl, $file);
        }
        $this->soap_server = new SoapServer($file, array( 'cache_wsdl' => WSDL_CACHE_NONE ));
        $this->soap_server->decode_utf8 = false;
        $this->generateClass( $main, $module );
        $this->soap_server->setClass('ActionJS');
        $this->main =& $main;
    }

    public function handle( $session_handler ) {
        global $log;
		$headers = headers_list();
		$sid = null;
		foreach ($headers as $header) {
			if (preg_match('/^X-Session: +(.+)$/', $header, $args)) {
				$sid = $args[1];
				break;
			}
		}
        $session = Session::factory($session_handler, $sid);
        header("X-Session: " . $session->session_id());
        ActionJS::$js = new JS($log, $session);
        ActionJS::$main =& $this->main;
        ActionJS::$log =& $log;
		ActionJS::$request = new Request();
        $a = new ActionJS();
		ob_start();
        $this->soap_server->handle();
		$response = ob_get_contents();
		ob_end_clean();
        $log->log("SOAP: return [$response]", PEAR_LOG_INFO);
        ActionJS::$js = null;
        return $response;
    }

    private function generateClass( &$main, $module ) {
		global $log;
        $class_data = 'class ActionJS {
            public static $main;
            public static $js;
            public static $log;
			public static $request;

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
        ';
        $funcs = $main->getFuncs($module);
        foreach ($funcs as $func => $data) {
            $class_data .= "public function $func() {
                self::\$request->params = func_get_args();
                \$code = self::\$main->getCode('$func', '$module');
                \$data = \$this->cleanup(self::\$js->evaluateScript(\$code[0]['code']));
                self::\$log->log('SOAP returns [' . print_r(\$data, true) . ']', PEAR_LOG_INFO);
                return \$data;
            } ";
        }
        $class_data .= "}";
        eval($class_data);
    }

    private function cacheGen($module, &$wsdl, $file) {
        $data = $wsdl->generate($module);
        $f = fopen($file, "wt");
        fwrite($f, $data);
        fclose($f);
    }

}
