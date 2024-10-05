<?php
require_once "../core/init.php";

$app= new App();
$app->obtenerDatos(PASSW); # PASSW must be defined in an "config.php" file outside public folder
?>