<?php

class Server {
    private $server;
    public function __construct() {
        global $_SERVER;
        $this->server =& $_SERVER;
    }
    public function __set( $key, $val ) {
        $this->server[$key] = $val;
    }
    public function __get( $key ) {
        return isset($this->server[$key]) ? $this->server[$key] : null;
    }
    public function __isset( $key ) {
        return isset($this->server[$key]);
    }
    public function __unset( $key ) {
        unset($this->server[$key]);
    }
}

