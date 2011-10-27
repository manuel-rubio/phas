<?php

chdir(__DIR__);

include_once(__DIR__ . "/../lib/PHAS.php");

$logfile = __DIR__ . "/../phas.log";
$database = array (
	"DSN" => "sqlite:/tmp/main.sqlite"
);

DataAccess::setDB(array ( "main" => $database ));
$main = DataAccess::singleton("main");

$script = <<<EOF

var spider = new DataAccess('euros');
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

$main->dml("INSERT INTO phas_phas( module, code, version, created_at ) VALUES ( ?, ?, ?, ? )", array ( array ( 'euros', $script, 1, date('Y-m-d H:i:s') ) ) );

$main->dml("INSERT INTO phas_databases( name, DSN ) VALUES ( 'euros', 'sqlite:../euros.sqlite' )");

$phas = new PHAS();
$phas->configureDB();

$euros = DataAccess::singleton('euros');
$euros->dml("CREATE TABLE monedas ( moneda char(3) not null primary key ); ANALYZE TABLE monedas;");
$euros->dml("CREATE TABLE valor_euro( moneda char(3) not null primary key, a_euros real not null, desde_euros real not null ); ANALYZE TABLE valor_euro;");

$euros->dml("INSERT INTO monedas(moneda) VALUES (?)", array(
	array ( 'USD' ), array ( 'GBP' ), array ( 'MXN' )
));
