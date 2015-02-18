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
$filename = (string)$_POST["filename"];
$SheetNum = (int)$_POST["SheetNum"];

//Does the file exist in the database?
if(!file_exists('Database//' . $filename)) {
	echo "<p><a href='index.php'>Home</a><br>ERROR: File not found: " . $filename . "</p>";
	exit(1);
}

//Call our python script and print out the excel file to the browser
echo shell_exec("python viewFile.py $filename $SheetNum 2>&1");
?>
