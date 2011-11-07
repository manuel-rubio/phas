<?php

class SoapGenerator {

    private $soap_server;
    private $main;

    public function __construct( $group, &$wsdl, &$main ) {
        global $wsdl_path, $wsdl_cache;
        $wsdl_cache = empty($wsdl_cache) ? 0 : $wsdl_cache;
        $wsdl_path = empty($wsdl_path) ? '/tmp' : $wsdl_path;
        $file = $wsdl_path . '/wsdl-api-' . $group;
        $f_cache = file_exists($file) ? stat($file) : array ( 'mtime' => 0 );
        if ($f_cache['mtime'] + $wsd_cache < time()) {
            $this->cacheGen($group, $wsdl, $file);
        }
        $this->soap_server = new SoapServer($file, array( 'cache_wsdl' => WSDL_CACHE_NONE ));
        $this->soap_server->decode_utf8 = false;
        $this->generateClass( $main, $group );
        $this->soap_server->setClass('ActionJS');
        $this->main =& $main;
    }

    public function handle( $session_handler ) {
        global $log;
        $sid = $this->request->SID;
        $session = Session::factory($session_handler, $sid);
        header("X-Session: " . $session->session_id());
        ActionJS::$js = new JS($log, $session);
        ActionJS::$request = new Request();
        ActionJS::$main =& $this->main;
        ActionJS::$log =& $log;

        $a = new ActionJS();
        $res = $this->soap_server->handle();
        $log->log("SOAP: return [$res]", PEAR_LOG_INFO);
        ActionJS::$js = null;
        return $res;
    }

    private function generateClass( &$main, $group ) {
        $class_data = 'class ActionJS {
            public static $main;
            public static $js;
            public static $request;
            public static $log;

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
        $funcs = $main->getFuncs($group);
        foreach ($funcs as $func => $data) {
            $class_data .= "public function $func() {
                self::\$request->params = func_get_args();
                \$code = self::\$main->getCode('$func', '$group');
                \$data = \$this->cleanup(self::\$js->evaluateScript(\$code[0]['code']));
                self::\$log->log('SOAP returns [' . print_r(\$data, true) . ']', PEAR_LOG_INFO);
                return \$data;
            } ";
        }
        $class_data .= "}";
        eval($class_data);
    }

    private function cacheGen($group, &$wsdl, $file) {
        $data = $wsdl->generate($group);
        $f = fopen($file, "wt");
        fwrite($f, $data);
        fclose($f);
    }

}
