<?php

class PHPSession extends Session {
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
		$this->session_id = session_id();
        $this->session =& $_SESSION;
    }
    public function __set( $key, $val ) {
        $this->session[$key] = $val;
    }
    public function __get( $key ) {
        return (isset($this->session[$key])) ? $this->session[$key] : null;
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
