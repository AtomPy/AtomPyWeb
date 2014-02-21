<?php
//Get our args
$Z = (string)$_POST["Z"];
$N = (string)$_POST["N"];

//Now get our file via our python download bot
$filename = (string)shell_exec("python download-bot.py $Z $N");
$filename = substr($filename, 0, -1);
if(strcmp($filename,'ERROR') != 0) {
	if(strcmp($filename,'FILE NOT FOUND') != 0) {
		//Now send the file to the browser
		header("Content-type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet");
		header("Content-Disposition: attachment; filename=$filename");
		header("Pragma: no-cache");
		header("Expires: 0");
		header("Content-Transfer-Encoding: binary");
		readfile('TempFiles\\' . $filename, true);
		unlink('TempFiles\\' . $filename);
	} else {
		print 'The file you requested was not found...';
	}
} else {
	print 'Something with wrong with the Python script...';
}

?>