<?php

class Request {
    private $request;
    public function __construct() {
        global $_REQUEST;
        $this->request =& $_REQUEST;
    }
    public function __set( $key, $val ) {
        $this->request[$key] = $val;
    }
    public function __get( $key ) {
        return isset($this->request[$key]) ? $this->request[$key] : null;
    }
    public function __isset( $key ) {
        return isset($this->request[$key]);
    }
    public function __unset( $key ) {
        unset($this->request[$key]);
    }
}

