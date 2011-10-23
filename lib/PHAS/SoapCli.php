<?php

class SoapCli {
    private $api;
    public function __construct( $wsdl ) {
        $this->api = new SoapClient($wsdl);
    }
    public function call( $method, $params ) {
        $p = array();
        if (is_object($params)) {
            foreach ($params as $param) {
                $p[] = $param;
            }
        }
        return $this->api->__call($method, $p);
    }
}

