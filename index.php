<?php
/* Index PHP for AtomPy 2.1
 *
 * Created by Josiah Lucas Boswell (www.josiahboswell.com)
 *
 * Homepage for AtomPy.
 */
 
 //Extra debugging  for PHP errors
ini_set('display_errors',1);
error_reporting(E_ALL);

?>

<!--Begin Homepage-->
<html>
<center>

<!--Homepage Title-->
<h2><b>AtomPy Website</b></h2>

<!--View File System-->
<h4>View Database Files</h4>
<p>Enter the Z and N values of the atomic files you wish to view.</p>
<form action="viewFile.php" method="get">
Z: <input type="text" name="Z" size="2">
N: <input type="text" name="N" size="2">
<input type="hidden" name="SheetNum" value="0">
<input type="hidden" name="BackupArg" value="-1"><br>
<br><input type="submit" value="View File">
</form><br><br>

<!--Download File System-->
<h4>Download Database Files</h4>
<p>Select the Z and N values of the atomic file you wish to download, then hit "Request File".</p>
<form action="downloadFile.php" method="get">
Z: <input type="text" name="Z" size="2">
N: <input type="text" name="N" size="2"><br>
<br><input type="submit" value="Request File">
</form><br><br>

<!--Upload File System-->
<h4>Upload File To Database</h4>
<p>Guidelines: Please follow these instructions for a perfect upload.<br>Step 1: Download a file from the database.<br>Step 2: Add your data. This can be either appending columns at the end of sheets or inserting rows.<br>Step 3: Add your source information to the AtomPy database (see below)<br>Step 4: At the top of the columns for your new data columns, add a hyperlink that is simply the number of the sourceID in the sources database of atompy.<br>Step 5: Upload the file and wait for it to be processed. This usually takes a few minutes.<br>Step 6: Check to see if your file upload was successful or not by checking the logs (see below).<br></p>
<form action="uploadFile.php" method="post" enctype="multipart/form-data">
<label for="file">Filename:</label>
<input type="file" name="file" id="file">
<input type="submit" value="Upload File">
</form><br><br>

<!--Add/View Sources System-->
<h4>Add/View Sources</h4>
<p><a href="sources.php">Click here to add/view sources.</a></p>
<br><br>

<!--Logs System-->
<h4>View Upload Log</h4>
<p><a href="logs.php">Click here to view upload logs.</a></p>
<br><br>

<!--End Homepage-->
</center>
</html>
