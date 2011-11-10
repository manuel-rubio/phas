<?php

class CacheMemcache implements ICache {
	private $memcache;
	private $expires;
	public function __construct() {
        global $cache_memcache_host, $cache_memcache_port, $cache_expires;
        if (!isset($cache_expires)) {
            $this->expires = 60; // a minute
        } else {
            $this->expires = $cache_expires;
        }
        $this->memcache = new Memcache();
        $this->memcache->connect($cache_memcache_host, $cache_memcache_port);
	}
    public function set( $key, $val ) {
        $this->memcache->set($key, serialize($val), 0, $this->expires);
    }
    public function get( $key, &$success ) {
		$data_raw = $this->memcache->get($key);
		$success = !($data_raw === FALSE);
        return unserialize($data_raw);
    }
}
