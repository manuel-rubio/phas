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

    public function getFuncs( $group ) {
        $funcs_raw = $this->conn->dql("
            SELECT p.module, a.name, t.xsd_name as param_type, r.name as return_type
            FROM phas_phas p
            LEFT JOIN phas_PhasAttrs a ON p.id = a.code_id
            LEFT JOIN phas_TAD t ON t.id = a.tad_id
            LEFT JOIN phas_TAD r ON r.id = p.return_attr_id
            WHERE p.version = ( SELECT MAX(version) FROM phas_phas WHERE id = p.id )
            AND p.group_id = ( SELECT id FROM phas_groups WHERE name = ? )
        ", array ( $group ));
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
                // TODO: falta el tipo 'doc' para la documentacion.
            }
        }
        return $funcs;
    }

}
