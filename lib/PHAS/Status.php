<html>
<head>
    <title>Status Info</title>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <script type="text/javascript" src="js/jquery.min.js"></script>
    <script type="text/javascript" src="js/jquery-ui.min.js"></script>
    <script type="text/javascript" src="js/status.js"></script>
    <link rel="stylesheet" href="status.css" type="text/css" media="all" />
</head>
<body>
    <h1>PHAS - Status Info</h1>
    <hr />
    <div id="content">
        <h3>Databases</h3>
        <div id="databases">
        <?php foreach ($INFO['databases'] as $name => $info) { ?>
        <h5 id="databases_<?=$name?>-header" class="nohighlight"><?=$name?></h5>
        <div id="databases_<?=$name?>-content">
            <table class="info">
            <?php foreach ($info as $key => $value) { ?>
            <tr>
                <th><?=$key?></th>
                <td><?=$value?></th>
            </tr>
            <?php } ?>
            </table>
        </div>
        <?php } ?>
        </div>

        <hr />
        <h3>Output Handlers</h3>
        <div id="salidas">
        <?php foreach ($INFO['output_handlers'] as $name => $info) { ?>
        <h5 id="salidas_<?=$name?>-header" class="nohighlight"><?=$name?></h5>
        <div id="salidas_<?=$name?>-content">
        <ul>
            <?php foreach ($info as $key => $value) { ?>
            <li><strong><?=$key?></strong>: <?=$value?></li>
            <?php } ?>
        </ul>
        </div>
        <?php } ?>
        </div>

        <hr />
        <h3>Code</h3>
        <div id="funciones">
            <?php foreach ($INFO['codes'] as $info) { ?>
            <h5 id="funciones_<?=$info['module']?>-header" class="nohighlight"><?=$info['module']?> (version <?=$info['version']?>)</h5>
            <div id="funciones_<?=$info['module']?>-content" class="scroll"></div>
            <?php } ?>
        </div>
    </div>
</body>
</html>