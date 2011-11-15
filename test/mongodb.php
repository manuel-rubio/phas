<?php

include(__DIR__ . "/../lib/PHAS/Session.php");

$mongo_server = 'localhost';
$session_expires = 2;

$sess = new MongoSession('aaaa');
$sess->dato = 'hola';
print $sess->dato . "\n";

$sess->dato = array ( 1,2,3,4 );
print_r($sess->dato); print "-------------\n";

$ses2 = new MongoSession('aaaa');

print_r($ses2->dato); print "-------------\n";

print "Sleeping 5 seconds...";
sleep(5);
print "\n";

$ses3 = new MongoSession('aaaa');

print_r($ses3->dato); print "-------------\n";

$sess->destroy();

print_r($ses3->dato); print "-------------\n";

