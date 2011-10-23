<?php

class JS {

    private $js;

    public function __construct( $log, $session_id = null ) {
        $js = new JSContext();
        $js->assign('session', new Session($session_id));
        $js->assign('request', new Request());

        $js->registerClass('SoapCli');
        $js->registerClass('DataAccess');

        $js->assign('logger', $log);
        $js->assign('PEAR_LOG_DEBUG', PEAR_LOG_DEBUG);
        $js->assign('PEAR_LOG_INFO', PEAR_LOG_INFO);
        $js->assign('PEAR_LOG_WARNING', PEAR_LOG_WARNING);
        $js->assign('PEAR_LOG_ERR', PEAR_LOG_ERR);
        $js->assign('PEAR_LOG_ALERT', PEAR_LOG_ALERT);
        $js->assign('PEAR_LOG_CRIT', PEAR_LOG_CRIT);
        $js->assign('PEAR_LOG_EMERG', PEAR_LOG_EMERG);
        $js->assign('PEAR_LOG_NOTICE', PEAR_LOG_NOTICE);
        $this->js = $js;
    }

    public function evaluateScript( $code ) {
        return $this->js->evaluateScript($code);
    }

}

