<html>
<center>
<h2><b>AtomPy Prototype Website</b></h2>
<h4>Download Files From Databases</h4>
<p>Enter the Z and N values of the atomic file you wish to download, then hit "Request File".</p>
<form action="downloadFile.php" method="post">
Z: <input type="text" name="Z" size="2">
N: <input type="text" name="N" size="2"><br><br>
<input type="radio" name="database" value="google" checked>Download from Google Drive<br>
<input type="radio" name="database" value="atompy">Download from AtomPy Database<br>
<br><input type="submit" value="Request File">
</form><br><br>
<h4>Upload Files To AtomPy Database</h4>
<p>Guidelines: TODO</p>
<form action="uploadFile.php" method="post" enctype="multipart/form-data">
<label for="file">Filename:</label>
<input type="file" name="file" id="file">
<input type="submit" value="Upload File">
</form><br><br>
<h4>View Files Through Browser</h4>
<form action="viewFile.php" method="post">
Z: <input type="text" name="Z" size="2">
N: <input type="text" name="N" size="2">
<input type="hidden" name="SheetNum" value="0">
<br><input type="submit" value="View File">
</form>
</center>
</html>