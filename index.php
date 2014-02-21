<html>
<center>
<h2><b>AtomPy Prototype Website</b></h2>
<h4>Download Files</h4>
<p>Enter the Z and N values of the atomic file you wish to download, then hit submit.</p>
<form action="downloadFile.php" method="post">
Z: <input type="text" name="Z" size="2">
N: <input type="text" name="N" size="2">
<br><input type="submit" value="Request File">
</form>
<h4>Upload Files</h4>
<form action="uploadFile.php" method="post" enctype="multipart/form-data">
<label for="file">Filename:</label>
<input type="file" name="file" id="file">
<input type="submit" value="Upload File">
</form>
</center>
</html>