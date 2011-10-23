<?php

class Session {
    private $session;
    public function __construct($session_id=null) {
        if ($session_id) {
            session_id($session_id);
        }
        session_start();
        $this->session =& $_SESSION;
    }
    public function __set( $key, $val ) {
        $this->session[$key] = $val;
    }
    public function __get( $key ) {
        return $this->session[$key];
    }
    public function __isset( $key ) {
        return isset($this->session[$key]);
    }
    public function __unset( $key ) {
        unset($this->session[$key]);
    }
    public function destroy() {
        session_destroy();
    }
}

