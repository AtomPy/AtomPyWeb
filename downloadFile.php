<?php
/* Download File PHP Script for AtomPy 2.1
 *
 * Created by Josiah Lucas Boswell (www.josiahboswell.com)
 *
 * Takes the Z and N args for the file the user wants. The filename is built and is searched for in the database. The file is then sent to
 * the user's browser for download.
 */
 
//Get our args (Z, N)
$Z = (int)$_GET["Z"];
$N = (int)$_GET["N"];

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

//Find out if the file exists in the database
if(!file_exists('Database//' . $filename)) {
	echo "<p><a href='index.php'>Home</a><br>ERROR: File not found: " . $filename . "</p>";
	exit(1);
}

//Send the file to the user's browser
header("Content-type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet");
header("Content-Disposition: attachment; filename=$filename");
header("Pragma: no-cache");
header("Expires: 0");
header("Content-Transfer-Encoding: binary");
readfile('Database//' . $filename, true);

?>
