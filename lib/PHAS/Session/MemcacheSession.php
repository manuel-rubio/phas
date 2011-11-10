<?php # -*- coding: utf-8 -*-

class MemcacheSession extends Session {
    private $memcache;
    private $expires;
    public function __construct( $session_id=null ) {
        global $session_memcache_host, $session_memcache_port, $session_expires;
        if (!isset($session_expires)) {
            $this->expires = 24 * 3600; // a day
        } else {
            $this->expires = $session_expires;
        }
        $this->memcache = new Memcache();
        $this->memcache->connect($session_memcache_host, $session_memcache_port);
        $this->session_id = (!$session_id) ? sha1(mt_rand()) : $session_id;
    }
    public function __set( $key, $val ) {
        $data = unserialize($this->memcache->get($this->session_id));
        if (!is_array($data)) {
            $data = array();
        }
        $data[$key] = $val;
        $this->memcache->set($this->session_id, serialize($data), 0, $this->expires);
    }
    public function __get( $key ) {
        $data = unserialize($this->memcache->get($this->session_id));
        if (!is_array($data) or !isset($data[$key])) {
            return null;
        }
        return $data[$key];
    }
    public function __isset( $key ) {
        $data = unserialize($this->memcache->get($this->session_id));
        if (!is_array($data) or !isset($data[$key])) {
            return false;
        }
        return true;
    }
    public function __unset( $key ) {
        $data = unserialize($this->memcache->get($this->session_id));
        if (is_array($data) and isset($data[$key])) {
            unset($data[$key]);
            $this->memcache->set($this->session_id, serialize($data), 0, $this->expires);
        }
    }
    public function destroy() {
        if (!empty($this->session_id)) {
            $this->memcache->set($this->session_id, '', 0, 1);
        }
    }

}
