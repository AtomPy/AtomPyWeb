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

	//Now call the verification/validation/hyperlink-adding/other stuffs script
	//This script is called as a background process so that the user does not have to wait
	exec("python uploadFile.py $filename >/dev/null &");

	//Return user to the homepage
	echo "<a href='index.php'>Home</a><br>Uploaded file queued. Please wait. You may check if your file was uploaded successfully via the logs on the home page.";
	
} else {
	echo "<a href='index.php'>Home</a><br>ERROR: The file you wish to upload is already in the processing folder. Please give the server a few minutes to catch up.";
}
?>
