<?php

class WSDLGenerator {

    private $types;
    private $mytypes;
    private $main;

    public function __construct( &$main ) {
        $this->main =& $main;
        $this->types = $main->getTypes();
        $this->mytypes = $main->getMyTypes( $this->types );
    }

    private function getType( $type, $min_max = false ) {
        $vector = "";
        $tipo_dato = "xsd:string";
        if (isset($this->types[$type])) {
            $tipo_dato = $this->types[$type];
        } elseif (isset($this->mytypes[$type])) {
            $tipo_dato = "tns:$type";
        } elseif (isset($this->mytypes["ArraOf$type"])) {
            $tipo_dato = "tns:ArrayOf$type";
        }
        return $tipo_dato;
    }

    private function element($name, $type, $min, $max) {
        return str_repeat(" ", 19) . "<element name=\"$name\" type=\"$type\" minOccurs=\"$min\" maxOccurs=\"$max\"/>\n";
    }

    private function complexType( $name, $elements ) {
        $elements_txt = "";
        foreach ($elements as $element) {
            list($type, $min, $max) = $this->getType($element['type'], true);
            $elements_txt .= $this->element($element['name'], $type, $min, $max);
        }
        return str_repeat(" ", 13) . "<complexType name=\"$name\">\n" .
               str_repeat(" ", 17) . "<sequence>\n" . $elements_txt .
               str_repeat(" ", 17) . "</sequence>\n" .
               str_repeat(" ", 13) . "</complexType>\n" .
               str_repeat(" ", 13) . "<complexType name=\"ArrayOf$name\">\n" .
               str_repeat(" ", 17) . "<complexContent>\n" .
               str_repeat(" ", 21) . "<restriction base=\"soapenc:Array\">\n" .
               str_repeat(" ", 25) . "<attribute ref=\"soapenc:arrayType\" wsdl:arrayType=\"tns:{$name}[]\" />\n" .
               str_repeat(" ", 21) . "</restriction>\n" .
               str_repeat(" ", 17) . "</complexContent>\n" .
               str_repeat(" ", 13) . "</complexType>\n";
    }

    private function message( $func, $params, $type_return ) {
        return str_repeat(" ", 5) . "<message name=\"{$func}Request\">\n" .
               $params . str_repeat(" ", 5) . "</message>\n" .
               str_repeat(" ", 5) . "<message name=\"{$func}Response\">\n" .
               str_repeat(" ", 9) . "<part name=\"{$func}Return\" type=\"$type_return\" />\n" .
               str_repeat(" ", 5) . "</message>\n";
    }

    private function part( $name, $type ) {
        return str_repeat(" ", 9) . "<part name=\"$name\" type=\"$type\" />\n";
    }

    private function operations_port( $func, $doc ) {
        return str_repeat(" ", 9) . "<operation name=\"$func\">\n" .
               str_repeat(" ", 13) . "<documentation>$doc</documentation>\n" .
               str_repeat(" ", 13) . "<input message=\"tns:{$func}Request\" />\n" .
               str_repeat(" ", 13) . "<output message=\"tns:{$func}Response\" />\n" .
               str_repeat(" ", 9) . "</operation>\n";
    }

    private function operations_bind( $module, $func ) {
        return str_repeat(" ", 9) . "<operation name=\"$func\">\n" .
               str_repeat(" ", 13) . "<soap:operation soapAction=\"\"/>\n" .
               str_repeat(" ", 13) . "<input>\n" .
               str_repeat(" ", 17) . "<soap:body use=\"encoded\" namespace=\"urn:$module\" encodingStyle=\"http://schemas.xmlsoap.org/soap/encoding/\"/>\n" .
               str_repeat(" ", 13) . "</input>\n" .
               str_repeat(" ", 13) . "<output>\n" .
               str_repeat(" ", 17) . "<soap:body use=\"encoded\" namespace=\"urn:$module\" encodingStyle=\"http://schemas.xmlsoap.org/soap/encoding/\"/>\n" .
               str_repeat(" ", 13) . "</output>\n" .
               str_repeat(" ", 9) . "</operation>\n";
    }

    public function generate($module) {
        global $wsdl_url;
        $ret = "";
        $funcs = $this->main->getFuncs($module);
        if (!empty($funcs)) {
            $types = "";
            foreach ($this->mytypes as $mytype => $parts) {
                $types .= $this->complexType($mytype, $parts);
            }
            $messages = "";
            $operations_port = "";
            $operations_bind = "";
            foreach ($funcs as $func => $data) {
                $type_return = $this->getType($data["return"]);
                $params_txt = "";
                if (is_array($data["params"]) and count($data["params"]) > 0) {
                    foreach ($data["params"] as $param) {
                        $type = $this->getType($param["type"]);
                        $params_txt .= $this->part($param['name'], $this->getType($param['type']));
                    }
                }
                $messages .= $this->message($func, $params_txt, $type_return);
                $operations_port .= $this->operations_port($func, $data['doc']);
                $operations_bind .= $this->operations_bind($module, $func);
            }
            $module_lower = strtolower($module);
            if (empty($wsdl_url)) {
                $wsdl_url = "http://" . $_SERVER['SERVER_NAME'] . ":" .
                    $_SERVER['SERVER_PORT'] . $_SERVER['PHP_SELF'] .
                    '?module=' . $module . '&#38;soap';
            }
            $ret = <<<EOF
<?xml version="1.0" encoding="UTF-8"?>
<definitions name="API"
        xmlns:xsd="http://www.w3.org/2001/XMLSchema"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns:soapenc="http://schemas.xmlsoap.org/soap/encoding/"
        xmlns:tns="urn:$module"
        xmlns:soap="http://schemas.xmlsoap.org/wsdl/soap/"
        xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/"
        xmlns="http://schemas.xmlsoap.org/wsdl/"
        targetNamespace="urn:$module">
    <types>
        <schema targetNamespace="urn:$module"
                xmlns="http://www.w3.org/2001/XMLSchema"
                xmlns:xsd="http://www.w3.org/2001/XMLSchema"
                xmlns:soap="http://schemas.xmlsoap.org/wsdl/soap/"
                xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/">
            <complexType name="ArrayOfString">
                 <complexContent>
                     <restriction base="soapenc:Array">
                         <attribute ref="soapenc:arrayType" wsdl:arrayType="xsd:string[]" />
                     </restriction>
                 </complexContent>
             </complexType>
             <complexType name="MatrixOfString">
                 <complexContent>
                     <restriction base="soapenc:Array">
                         <attribute ref="soapenc:arrayType" wsdl:arrayType="tns:ArrayOfString[]" />
                     </restriction>
                 </complexContent>
             </complexType>
$types
        </schema>
    </types>
$messages
    <portType name="APIPortType">
$operations_port
    </portType>
    <binding name="APIBinding" type="tns:APIPortType">
        <soap:binding style="rpc" transport="http://schemas.xmlsoap.org/soap/http"/>
$operations_bind
    </binding>
    <service name="APIService">
        <port name="APIPort" binding="tns:APIBinding">
            <soap:address xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/"
            location="$wsdl_url"/>
        </port>
    </service>
</definitions>
EOF;
        }
        return $ret;
    }
}
