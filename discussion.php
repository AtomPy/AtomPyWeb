<?php

//Extra debugging  for PHP errors
ini_set('display_errors',1);
error_reporting(E_ALL);

if(isset($_GET["Z"])) {
	echo "Z: " . $_GET["Z"] . "N: " . $_GET["N"] . "Sheet: " . $_GET["Sheet"] . "Row: " . $_GET["Row"] . "Col: " . $_GET["Col"];
}
?>
