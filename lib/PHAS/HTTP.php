<?php

class HTTP {
    private $http;
    public function __construct( $url, $method = 'GET' ) {
        switch ($method) {
            case "POST": $method = HttpRequest::METH_POST; break;
            case "GET":
            default: $method = HttpRequest::METH_GET;
        }
        $this->http = new HttpRequest($url, $method);
    }

    public function send() {
        try {
            $this->http->send();
        } catch (Exception $e) {
            return false;
        }
        return true;
    }

    public function getBody() {
        return $this->http->getResponseBody();
    }

    public function getCode() {
        return $this->http->getResponseCode();
    }

    public function addQueryData( $key, $value ) {
        $this->http->addQueryData(array ( $key => $value ));
    }

    public function addPostField( $key, $value ) {
        $this->http->addPostFields(array ( $key, $value ));
    }

    public function addPostRawData( $data ) {
        $this->http->addRawPostData($data);
    }

    public function addCookieData( $key, $value ) {
        $this->http->addCookies(array ( $key => $value ));
    }

}

