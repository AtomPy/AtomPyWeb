<?php
/* Upload File PHP Script for AtomPy 2.0
 * Created by Josiah Lucas Boswell (www.josiahboswell.com)
 * Takes a user-submitted file, moves it to a temporary
 * location, and passes the file info to a python script.
 * If the python script returns successfully, the backup
 * program is called. The temporary file is deleted in
 * the end.
 */
 
ini_set('display_errors',1);
error_reporting(E_ALL);

//Get the uploaded files temp location
$tempLocation = $_FILES["file"]["tmp_name"];

//Get our filename
$filename = $_FILES["file"]["name"];

//Pass the filename to the python script for processing
$result = (string)shell_exec("python newUploadFile.py $filename $tempLocation 2>&1");
echo 'called\n';

//See if the upload was successful
if(strstr($result, 'ERROR')) {
	echo $result;
} else {
	echo $result;
	//Call the backup program
	echo shell_exec("python NewBackupBot.py");
	
	//Print Success
	echo "SUCCESSFULLY UPLOADED FILE!";
}
echo 'ended\n';
?>
