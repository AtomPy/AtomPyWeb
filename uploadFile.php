<?php
	//Get the uploaded files temp location
	$tempLocation = $_FILES["file"]["tmp_name"];
	
	//Get our filename
	$filename = $_FILES["file"]["name"];
	
	//Save the temp file to a nicer place
	move_uploaded_file($tempLocation, "TempFiles\\" . $filename);
	
	//Pass the filename to the python script for processing
	$result = (string)shell_exec("python newUploadFile.py $filename");
	
	//See if the upload was successful
	if(strstr($result, 'ERROR')) {
		echo $result;
	} else {
		//Call the backup program
		echo shell_exec("python NewBackupBot.py");
		
		//Print Success
		echo "SUCCESSFULLY UPLOADED FILE!";
	}
	
	//Delete the uploaded file from tempFiles
	unlink("TempFiles\\" . $filename);
?>
