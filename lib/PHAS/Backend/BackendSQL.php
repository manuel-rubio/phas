<?php

class BackendSQL {
	
	private $conn;
	
	public function __construct() {
		global $database;
	    DataAccess::setDB(array ( "main" => $database ));
	    $this->conn = DataAccess::singleton('main');
	}

	public function getCode( $module, $group ) {
		return $this->conn->dql("
	        SELECT code
	        FROM phas_phas p LEFT JOIN phas_groups g ON p.group_id = g.id
	        WHERE module = ? AND name = ?
	        ORDER BY version DESC
	    ", array ( $module, $group ));
	}
	
	public function getDB() {
		return $this->conn->dql("
	        SELECT id, name, DSN, USR, PWD
	        FROM phas_databases
	    ");
	}
}
