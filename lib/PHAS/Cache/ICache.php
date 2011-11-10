<?php

interface ICache {
	public function get($key, &$success);
	public function set($key, $value);
}
