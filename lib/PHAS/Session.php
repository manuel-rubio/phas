<?php

include_once(__DIR__ . "/Session/PHPSession.php");
include_once(__DIR__ . "/Session/MongoSession.php");

class Session {

    private $session;

    public function factory( $handler, $sid = null ) {
        if (!isset($this->session[$handler])) {
            $this->session[$handler] = new $handler($sid);
        }
        return $this->session[$handler];
    }

}

