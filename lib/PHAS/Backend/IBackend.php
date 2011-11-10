<?php

interface IBackend {

	public function getCode( $module, $group );
	public function getDB();
	public function getTypes();
    public function getMyTypes( $types );
    public function getFuncs( $group );
	
}
