<?php
/* Download File PHP Script for AtomPy 2.0
 * Created by Josiah Lucas Boswell (www.josiahboswell.com)
 * Takes arguements for the file the user wants and either
 * downloads the file from Google Drive or finds it in the
 * local AtomPy database. The file is then pushed to the
 * browser.
 */
 
//Get our args
$Z = (string)$_POST["Z"];
$N = (string)$_POST["N"];
$database = (string)$_POST["database"];

//Now get our file via our python download bot
$filename = (string)shell_exec("python download-bot.py $Z $N $database");
$filename = substr($filename, 0, -1);
if(!strstr($filename, 'ERROR')) {
	//Now send the file to the browser
	header("Content-type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet");
	header("Content-Disposition: attachment; filename=$filename");
	header("Pragma: no-cache");
	header("Expires: 0");
	header("Content-Transfer-Encoding: binary");
	if(strstr($database,'google')) {
		readfile('TempFiles//' . $filename, true);
		unlink('TempFiles//' . $filename);
	}
	if(strstr($database,'atompy')) {
		readfile('Database//' . $filename, true);
	}
	
} else {
	print $filename;
}

?>