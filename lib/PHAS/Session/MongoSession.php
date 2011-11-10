<?php

class MongoSession extends Session {
    private $collect;
    private $expires;
    private static $conn;
    public function __construct($session_id=null) {
        global $mongo_server, $session_expires;
        if (!isset($mongo_server)) {
            $mongo_server = "localhost";
        }
        if (!isset($session_expires)) {
            $this->expires = 24 * 3600; // a day
        } else {
            $this->expires = $session_expires;
        }
        if (!isset(self::$conn)) {
            self::$conn = new Mongo($mongo_server);
        }
        $sid = (!$session_id) ? sha1(mt_rand()) : $session_id;
        $this->session_id = $sid;
        $this->collect = self::$conn->session->$sid;
        $this->collect->ensureIndex( array ( "key" => 1 ) );
        $this->collect->ensureIndex( array ( "ts" => 1 ) );
        $this->gc();
    }
    public function gc() {
        $this->collect->remove(array ( "ts" => array ( '$lte' => time() )));
    }
    public function __set( $key, $val ) {
        $ts = time() + $this->expires;
        if (isset($this->$key)) {
            $this->collect->update(array("key" => $key), array("key" => $key, "val" => $val, "ts" => $ts));
        } else {
            $this->collect->insert(array ( "key" => $key, "val" => $val, "ts" => $ts ));
        }
    }
    public function __get( $key ) {
        $cursor = $this->collect->find( array ( "key" => $key ));
        if ($cursor->hasNext()) {
            $data = $cursor->getNext();
            return $data['val'];
        }
        return null;
    }
    public function __isset( $key ) {
        $cursor = $this->collect->find( array ( "key" => $key ) );
        return ($cursor->hasNext());
    }
    public function __unset( $key ) {
        $this->collect->remove(array ( "key" => $key ));
    }
    public function destroy() {
        $this->collect->drop();
    }
}
