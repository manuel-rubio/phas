<?php

include_once(__DIR__ . '/Cache/ICache.php');
include_once(__DIR__ . '/Cache/CacheAPC.php');
include_once(__DIR__ . '/Cache/CacheMemcache.php');

class Cache {

	public static function &factory( $handler ) {
		switch ($handler) {
			case "APC":      $c = new CacheAPC(); break;
			case "MEMCACHE": $c = new CacheMemcache(); break;
			case "NONE":
			default:
				// no se hace nada
				$c = false;
		}
		return $c;
	}
	
}
