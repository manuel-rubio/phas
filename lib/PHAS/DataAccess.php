<?php

class DataAccess {
    private $pdo;
	private $cache;
    private static $databases;
	private static $conn;

	public static function singleton( $name, $cache=false ) {
		if (isset(self::$databases[$name])) {
		 	if (!isset(self::$conn[$name])) {
				self::$conn[$name] = new DataAccess($name, $cache);
			}
			return self::$conn[$name];
		}
		return false;
	}
    public static function setDB( $databases ) {
        self::$databases = $databases;
    }
    public function __construct( $name, $cache=false ) {
        if (!isset(self::$databases[$name])) {
            throw new Exception("database [$name] not found, only: " . serialize(self::$databases));
        }
        $db = self::$databases[$name];
        if (preg_match("/^sqlite/", $db["DSN"])) {
            $this->pdo = new PDO($db["DSN"]);
        } else {
            $this->pdo = new PDO($db["DSN"], $db["USR"], $db["PWD"]);
        }
		if ($cache) {
			$this->cache = Cache::factory($cache);
		}
    }
    public function dql( $sql, $params = array() ) {
        $p = array();
        if (is_object($params)) {
            foreach ($params as $param) {
                $p[] = $param;
            }
        } else {
            $p = $params;
        }
		$key = 'sql/' . md5($sql . serialize($p));
		if ($this->cache) {
			$data = $this->cache->get($key, $succ);
			if ($succ) {
				return $data;
			}
		}
        $sth = $this->pdo->prepare($sql);
        if ($sth instanceof PDOStatement) {
            $sth->execute($p);
            $response = $sth->fetchAll(PDO::FETCH_ASSOC);
			if ($this->cache) {
				$this->cache->set($key, $response);
			}
			return $response;
        }
        $errno = $this->pdo->errorCode();
        $errtxt = $this->pdo->errorInfo();
        throw new Exception("ERROR[$errno]: {$errtxt[2]}");
    }
    public function dml( $sql, $params = array() ) {
        $p = array();
        if (is_object($params)) {
            $i = 0;
            foreach ($params as $param) {
                if (is_object($param)) {
                    $j = 0;
                    foreach ($param as $element) {
                        $p[$i][$j++] = $element;
                    }
                } else {
                    $p[$i] = $param;
                }
                $i++;
            }
        } elseif (is_array($params)) {
            $p = $params;
        }
        $sth = $this->pdo->prepare($sql);
        if ($sth) {
            if (!is_array($params) or count($p) == 0) {
                $sth->execute();
            } else {
                foreach ($p as $e) {
                    $sth->execute($e);
                }
            }
        } else {
            $errno = $this->pdo->errorCode();
            $errtxt = $this->pdo->errorInfo();
            throw new Exception("ERROR[$errno]: {$errtxt[2]}");
        }
    }
}
