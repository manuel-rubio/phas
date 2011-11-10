<?php

include_once(__DIR__ . "/Session/PHPSession.php");
include_once(__DIR__ . "/Session/MongoSession.php");
include_once(__DIR__ . "/Session/MemcacheSession.php");

class Session {

    private $session;
	protected $session_id;

    public function &factory( $handler, $sid = null ) {
        if (!isset($this->session[$handler])) {
            $this->session[$handler] = new $handler($sid);
        }
        return $this->session[$handler];
    }

    public function session_id() {
		return $this->session_id;
	}
	public function gc() {}
}
