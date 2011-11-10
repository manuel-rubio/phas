<?php

include_once(__DIR__ . '/Backend/IBackend.php');
include_once(__DIR__ . '/Backend/BackendSQL.php');
include_once(__DIR__ . '/Backend/BackendMongo.php');

class Backend {
	
	private static $conn = array();
	
	public static function &factory() {
		global $database;
		$conn = $database['DSN'];
		if (!isset(self::$conn[$conn])) {
			list($con, $dummy) = explode(':', $database['DSN']);
			switch ($con) {
				case "sqlite":
				case "mysql":
				case "pgsql":
				case "mssql":
				case "sqlite3":
				case "dblib":
				case "oracle":
					self::$conn[$conn] = new BackendSQL();
					break;
				case "mongo":
				case "mongodb":
					self::$conn[$conn] = new BackendMongo();
					break;
				default:
					throw new Exception('ERROR: invalid backend or not defined in $database var.');
			}
		}
		return self::$conn[$conn];
	}
	
}
