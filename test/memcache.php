<?php

include(__DIR__ . "/../lib/PHAS/Session/MemcacheSession.php");

$memcache_host = 'localhost';
$memcache_port = "11211";
$session_expires = 2;

$sess = new MemcacheSession('aaaa');
$sess->dato = 'hola';
print $sess->dato . "\n";

$sess->dato = array ( 1,2,3,4 );
print_r($sess->dato); print "-------------\n";

$ses2 = new MemcacheSession('aaaa');

print_r($ses2->dato); print "-------------\n";

print "Sleeping 5 seconds...";
sleep(5);
print "\n";

$ses3 = new MemcacheSession('aaaa');

print_r($ses3->dato); print "-------------\n";

$sess->destroy();

print_r($ses3->dato); print "-------------\n";

