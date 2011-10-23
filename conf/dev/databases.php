<?php

$databases = array (
    "main" => array (
        "DSN" => "sqlite:" . __DIR__ . "/../../main.sqlite",
    ),
    "spidermonkey" => array (
        "DSN" => "pgsql:host=localhost;dbname=spidermonkey",
        "USR" => "spidermonkey",
        "PWD" => "spider2011",
    )
);

