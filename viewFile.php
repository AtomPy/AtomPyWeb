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
$Z = (int)$_GET["Z"];
$N = (int)$_GET["N"];
$SheetNum = (int)$_GET["SheetNum"];
$BackupArg = (int)$_GET["BackupArg"];

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
} else echo $filename . '<br>';

//Does the file have backups avaliable?
$backups = "";
foreach (glob($filename) as $filenames_found) {
	echo $filenames_found . "<br>";
}

//Call our python script and print out the excel file to the browser
echo shell_exec("python viewFile.py $Z $N $SheetNum $BackupArg $backups 2>&1");
?>
