<?php

class CacheAPC implements ICache {
	private $expires;
	public function __construct() {
        global $cache_expires;
        if (!isset($cache_expires)) {
            $this->expires = 60; // a minute
        } else {
            $this->expires = $cache_expires;
        }
	}
	public function get( $key, &$success ) {
		return apc_fetch($key, $success);
	}
	
	public function set( $key, $value ) {
		apc_store($key, $value, $this->expires);
	}
}
