<?php
/* Upload File PHP Script for AtomPy 2.1
 *
 * Created by Josiah 'Lucas' Boswell (www.josiahboswell.com)
 *
 * Takes a user submitted file from a POST operation. The temporary file name is passed to the validation bot for data checking.
 * If the validation bot returns without error, the backup bot is then called. After it is done, the user is returned to the homepage
 * with a success message.
 */

//Extra debugging  for PHP errors
ini_set('display_errors',1);
error_reporting(E_ALL);

//Get the file location and file name
$filelocation = $_FILES["file"]["tmp_name"];
$filename = $_FILES["file"]["name"];

//Make sure the file trying to be uploaded is not already in the uploads folder and thus not already being processed
if(!file_exists('Uploads/' . $filename)) {

	//Move the file from the default upload file location to the real uploads folder
	move_uploaded_file($filelocation, 'Uploads/' . $filename);

	//Fix permissions so that the new file isn't write-only
	chmod('Uploads/' . $filename, 0777);

	//Validate the file (java script)
	$arg0 = "validateFile";
	$arg1 = "Database//" . $filename;
	$arg2 = "Uploads//" . $filename;
	$result = shell_exec("java -jar AtomPyServer.jar $arg0 $arg1 $arg2 2>&1");
	if (strpos($result,'ERROR') !== false) {
		echo 'Something with validation of the file went wrong:<br>';
		echo $result;
	} else {
		
		//Backup the original file (python script)
		exec("python backupFile.py $filename  >/dev/null &");
		
		//Move the new file to the database
		rename('Uploads/' . $filename, 'Database/' . $filename);
		
		//Force-format the new file (java script)
		$arg0 = "formatFile";
		$arg1 = "Database//" . $filename;
		$result = shell_exec("java -jar AtomPyServer.jar $arg0 $arg1 2>&1");
		
		//Return user to the homepage
		echo "<a href='https://athena.physics.wmich.edu?page_id=145'>Return</a><br>File uploading! Please allow a few minutes for the file to be properly processed into the database.";
	
	}
	
} else {
	echo "You shouldn't be seeing this message. If you are, contact the server admin.";
}
?>
