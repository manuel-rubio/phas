<?php

class BackendSQL implements IBackend {

	private $conn;

	public function __construct() {
		global $database;
	    DataAccess::setDB(array ( "main" => $database ));
	    $this->conn = DataAccess::singleton('main');
	}

	public function getCode( $code, $module ) {
		return $this->conn->dql("
	        SELECT v.content as code
	        FROM phas_codes p 
			LEFT JOIN phas_modules m ON p.module_id = m.id
			LEFT JOIN phas_codeversions v ON v.code_id = p.id
	        WHERE m.name = ? AND p.name = ?
	        ORDER BY v.version DESC
	    ", array ( $module, $code ));
	}

	public function getDB() {
		return $this->conn->dql("
	        SELECT id, name, DSN, USR, PWD
	        FROM phas_databases
	    ");
	}

	public function getTypes() {
        $raw = $this->conn->dql("
            SELECT name, xsd_name
            FROM phas_TAD
            WHERE complex = 0
        ");
        $types = array();
        if (is_array($raw) and count($raw) > 0) {
            foreach ($raw as $data) {
                $types[$data['name']] = $data['xsd_name'];
            }
        }
        return $types;
    }

    public function getMyTypes( $types ) {
        $raw = $this->conn->dql("
            SELECT t.name, t.xsd_name, a.name AS attr_name
            FROM phas_TAD t
            LEFT JOIN phas_TADAttrs a ON t.id = a.tad_id
            WHERE complex = 1
        ");
        $mytypes = array();
        if (is_array($raw) and count($raw) > 0) {
            foreach ($raw as $data) {
                $mytypes[$data['name']]['xsd_name'] = $data['xsd_name'];
                if (!isset($types[$data['name']]['attrs'])) {
                    $mytypes[$data['name']]['attrs'] = array ();
                }
                if (!empty($data['attr_name'])) {
                    $mytypes[$data['name']]['attrs'][] = array (
                        'name' => $data['attr_name'],
                        'type' => $data['type'],
                        'dim' => $data['dim']
                    );
                }
            }
        }
        return $mytypes;
    }

    public function getFuncs( $module ) {
        $funcs_raw = $this->conn->dql("
            SELECT p.name AS module, a.name, p.doc, t.xsd_name as param_type, r.name as return_type
            FROM phas_codes p
            LEFT JOIN phas_CodeAttrs a ON p.id = a.code_id
            LEFT JOIN phas_TAD t ON t.id = a.tad_id
			LEFT JOIN phas_codeversions v ON p.id = v.code_id
            LEFT JOIN phas_TAD r ON r.id = v.return_attr_id
            WHERE p.version = v.version
            AND p.module_id = ( SELECT id FROM phas_modules WHERE name = ? )
        ", array ( $module ));
        $funcs = array();
        if (is_array($funcs_raw) and count($funcs_raw) > 0) {
            foreach ($funcs_raw as $func) {
                $funcs[$func['module']] = array(
                    'params' => array (),
                    'return' => 'xsd:string'
                );
                if (!empty($func['name']) and !empty($func['param_type'])) {
                    $funcs[$func['module']]['params'][$func['name']] = $func['param_type'];
                }
                if (!empty($func['return_type'])) {
                    $funcs[$func['module']]['return'] = $func['return_type'];
                }
				$funcs[$func['module']]['doc'] = $func['doc'];
            }
        }
        return $funcs;
    }

}
