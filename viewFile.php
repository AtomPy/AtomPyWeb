<?php
/* View File PHP Script for AtomPy 2.1
 *
 * Created by Josiah Lucas Boswell (www.josiahboswell.com)
 *
 * Takes a filename and sheet number as arguements and sends them to the viewFile python script. 
 * The excel file is then displayed.
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
//Error handling
ini_set('display_errors',1);
error_reporting(E_ALL);

//Get our args from PHP
$Z = (int)$_POST["Z"];
$N = (int)$_POST["N"];
$SheetNum = (int)$_POST["SheetNum"];
$BackupArg = (int)$_POST["BackupArg"];

//Validate numbers
if($Z < 0) $Z = 0;
if($N < 0) $N = 0;

//Build the filename
$filename = '';
if($Z < 10) $filename = $filename . '0' . (string)$Z;
else $filename = $filename . (string)$Z;
$filename = $filename . '_';
if($N < 10) $filename = $filename . '0' . (string)$N;
else $filename = $filename . (string)$N;
$filename = $filename . '.xlsx';

//Does the file exist in the database?
if(!file_exists('Database//' . $filename)) {
	echo "<p><a href='index.php'>Home</a><br>ERROR: File not found: " . $filename . "</p>";
	exit(1);
}

//Does the file have backups avaliable?
$backups = array();

//Open the mysql database
$conn = new mysqli("localhost","josiah","broncos131","atompy");
if($conn->connect_error) {
	die("Connection failed: " . $conn->connect_error);
}
$sql = "select * from backup where file='" . $filename . "'";
$result = $conn->query($sql);
if($result->num_rows > 0) {
	while($row = $result->fetch_assoc()) {
		array_push($backups, $row["backupDateTime"]);
	}
}

//Call our python script and print out the excel file to the browser
echo shell_exec("python viewFile.py $filename $SheetNum $BackupArg" . escapeshellarg(json_encode($backups)));
