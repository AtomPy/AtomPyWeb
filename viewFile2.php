<?php
/* View File PHP Script for AtomPy 2.1
 *
 * Created by Josiah Lucas Boswell (www.josiahboswell.com)
 *
 * Takes queries and sends them to the python script.
 */
?>
<style>
table,th,td
{
border:1px solid black;
border-collapse:collapse;
padding:5px;
}
</style>
<a href="index.php">Home</a>
<?php
ini_set('display_errors',1);
error_reporting(E_ALL);

//Open the mysql database
$conn = new mysqli("localhost","josiah","broncos131","atompy");
if($conn->connect_error) {
	die("Connection failed: " . $conn->connect_error);
} else echo 'SUCCESS<br>';
/*
//Get our args
$Z = (string)$_POST["Z"];
$N = (string)$_POST["N"];
$SheetNum = (int)$_POST["SheetNum"];
$BackupArg = (string)$_POST["BackupArg"];
*/
//Now get our file via our python download bot
//$result = shell_exec("python WebAPI.py $Z $N $SheetNum $BackupArg 2>&1");
//echo $result;
$sql = "show tables";
$result = $conn->query($sql);
if($result->num_rows > 0) {
	while($row = $result->fetch_assoc()) {
		echo $row['Tables_in_atompy'];
	}
}

$sql = "select * from backup";
$result = $conn->query($sql);
if($result->num_rows > 0) {
	while($row = $result->fetch_assoc()) {
		print_r($row);
	}
}
?>
