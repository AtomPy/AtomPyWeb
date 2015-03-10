<?php
/* getSource File PHP Script for AtomPy 2.1
 *
 * Created by Josiah 'Lucas' Boswell (www.josiahboswell.com)
 *
 * Takes a get request for the source value.
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

if(isset($_GET["sourceID"])) {
	
	#Look for the link or title already in the source table
	$sql = "select * from source where id=" . $_GET["sourceID"];
	$result = $conn->query($sql);
	if($result->num_rows > 0) {
		while($row = $result->fetch_assoc()) {
			echo $row["title"] . ', ' . $row["link"] . "<br>";
		}
	}
}

?>
</html>