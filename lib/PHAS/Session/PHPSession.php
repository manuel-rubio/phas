<?php

class PHPSession {
    private $session;
    public function __construct($session_id=null) {
        global $session_expires;
        if ($session_id) {
            session_id($session_id);
        }
        if ($session_expires) {
            session_cache_expire(round($session_expires/60));
        }
        session_start();
        $this->session =& $_SESSION;
    }
    public function gc() {
    }
    public function session_id() {
        return session_id();
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

