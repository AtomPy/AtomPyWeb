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

//Open the mysql database
$conn = new mysqli("localhost","josiah","broncos131","atompy");
if($conn->connect_error) {
	die("Connection failed: " . $conn->connect_error);
}

if(isset($_GET["workbook"]) and isset($_GET["sheet"]) and isset($_GET["row"]) and isset($_GET["col"])) {
	
	#Select the appropriate table entry and display it
	$sql = "select * from numberMetadata where workbook='" . $_GET["workbook"] . "' and sheet='" . $_GET["sheet"] . "' and row=" . $_GET["row"] . " and col=" . $_GET["col"];
	$result = $conn->query($sql);
	if($result->num_rows > 0) {
		while($row = $result->fetch_assoc()) {
			echo 'Result for the following: <br><br>Workbook: ' . $row['workbook'] . "<br>Sheet: " . $row["sheet"] . '<br>Row: ' . $row['row'] . '<br>Column: ' . $row['col'] . '<br><br>Number Value: ' . $row['numberValue'] . '<br>SourceID: <a href="http://141.218.60.56/~jnz1568/getSource.php?sourceID=' . $row['sourceID'] . '">' . $row['sourceID'] . '</a><br>Blog Link: ' . $row['blogLink'];
		}
	}
} else {
	echo 'Incorrect args or lack of args.<br>';
	print_r($_GET);
}

?>
</html>
