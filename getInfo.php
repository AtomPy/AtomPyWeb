<?php
/* getSource File PHP Script for AtomPy 2.1
 *
 * Created by Josiah 'Lucas' Boswell (www.josiahboswell.com)
 *
 * Takes a series of GET requests. The full hyperlink looks like:
 * 141.218.60.56/~jnz1568/info.php?wb=01_01.xlsx&sheet=E0&row=5&col=5
 *
 * Then returns a nice output of information on a webpage.
 */

//Extra debugging  for PHP errors
ini_set('display_errors',1);
error_reporting(E_ALL);

?>

<html>
<a href='index.php'>Home</a><br>

<?php

if(isset($_GET["workbook"]) and isset($_GET["sheet"]) and isset($_GET["row"]) and isset($_GET["col"]) and isset($_GET["number"]) and isset($_GET["sourceID"])) {
	
	#Display the args in a nice fasion
	echo 'Workbook: ' . $_GET['workbook'] . "<br>Sheet: " . $_GET["sheet"] . '<br>Row: ' . $_GET['row'] . '<br>Column: ' . $_GET['col'] . '<br>Number Value: ' . $_GET['numberValue'] . '<br>SourceID: <a href="http://141.218.60.56/~jnz1568/getSource.php?sourceID=' . $_GET['sourceID'] . '">' . $_GET['sourceID'] . '</a><br>Blog Link: Coming soon';
	
} else {
	echo 'Incorrect args or lack of args. Please double check your GET requests.<br>';
	print_r($_GET);
}

?>
</html>
