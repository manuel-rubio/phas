<?php

class BackendMongo implements IBackend {

	public function __construct() {
	}

	public function getCode( $module, $group ) {
		return "";
	}

	public function getDB() {
		return array();
	}

    public function getTypes() {
    }

    public function getMyTypes( $types ) {
    }

    public function getFuncs( $group ) {
    }

}
