<?php
	//Find out where our file is located in temp memory
	$file = $_FILES["file"]["tmp_name"];
	$filename = $_FILES["file"]["name"];
	
	//Pass the file to the python script for processing
	echo shell_exec("python uploadFile.py $file $filename");
?>
