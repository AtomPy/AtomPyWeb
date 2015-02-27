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

//Send the file to the validation bot
$result = (string)shell_exec("python validationBot.py $filename $tempLocation 2>&1");

//See if the upload was successful
if(strstr($result, 'ERROR')) {
	echo $result;
	exit(1);
}

//Call the backup bot
//$result = (string)shell_exec("python backupBot.py 2>&1");

//Return user to the homepage
echo "<a href='index.php'>Home</a><br>SUCCESSFULLY UPLOADED FILE!";
?>
