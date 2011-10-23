<?php

include_once(__DIR__ . "/../src/PHAS.php");
include_once(__DIR__ . "/../conf/config.php");
include_once(__DIR__ . "/../conf/$env/config.php");
include_once(__DIR__ . "/../conf/$env/databases.php");

if (!isset($databases['main'])) {
    throw new Exception("ERROR: entorno [$env] no valido.");
} 

DataAccess::setDB($databases);
$main = new DataAccess("main");

$script = <<<EOF

var spider = new DataAccess('spidermonkey');
var monedas = spider.dql('SELECT * FROM monedas');

var url = 'http://www.webservicex.net/CurrencyConvertor.asmx?WSDL';
var api = new SoapCli(url);
var convs = new Object();

for (var i in monedas) {
    var conversion;
    var moneda = monedas[i].moneda;
    convs[moneda] = new Object();

    logger.log("Moneda: " + moneda, PEAR_LOG_DEBUG);
    ConversionRate = {
        FromCurrency : moneda,
        ToCurrency: "EUR"
    }

    conversion = api.call("ConversionRate", [ConversionRate]);
    logger.log('resultado: ' + conversion.ConversionRateResult, PEAR_LOG_INFO);
    convs[moneda]['a_euros'] = conversion.ConversionRateResult;

    ConversionRate = {
        FromCurrency : "EUR",
        ToCurrency: moneda
    }

    conversion = api.call("ConversionRate", [ConversionRate]);
    logger.log('resultado: ' + conversion.ConversionRateResult, PEAR_LOG_INFO);
    convs[moneda]['desde_euros'] = conversion.ConversionRateResult;

    spider.dml('DELETE FROM valor_euro WHERE moneda = ?', [[ moneda ]] );
    spider.dml('INSERT INTO valor_euro (moneda, a_euros, desde_euros) VALUES (?, ?, ?)', 
               [[ moneda, convs[moneda]['a_euros'], convs[moneda]['desde_euros'] ]] );

}

logger.log('resultado: ' + convs.toSource());
logger.log('finalizado.', PEAR_LOG_INFO);

convs;
EOF;

$main->dml("INSERT INTO phas_phas( module, code, version, created_at ) VALUES ( ?, ?, ?, ? )", array ( array ( 'euros', $script, 0, date('Y-m-d H:i:s') ) ) );

