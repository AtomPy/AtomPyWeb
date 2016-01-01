<?php
/* Sources File PHP Script for AtomPy 2.1
 *
 * Created by Josiah 'Lucas' Boswell (www.josiahboswell.com)
 *
 * Allows a user to view and add sources to the database. Also allows for a request of a sourceID.
 */

//Extra debugging  for PHP errors
ini_set('display_errors',1);
error_reporting(E_ALL);
?>

<html>
<a href='index.php'>Home</a><br><br>

<h4>Find Source</h4>
<p>If you are curious if a source is already in the database, submit the link here.</p>
<form action="sources.php" method="post">
Link: <input type="text" name="linky" size="100"><br>
<input type="submit" value="Find Source">
</form>

<h4>Add Source</h4>
<p>Add a source to the database by submitting a link and title for the given source.</p>
<form action="sources.php" method="post">
Title: <input type="text" name="title" size="100"><br>
Link: <input type="text" name="link" size="100"><br>
<input type="submit" value="Add Source">
</form>

<?php
//Open the mysql database
$conn = new mysqli("localhost","josiah","broncos131","atompy");
if($conn->connect_error) {
	die("Connection failed: " . $conn->connect_error);
}

if(isset($_POST["title"])) {
	if(isset($_POST["link"])) {
	
		if($_POST["title"] != '') {
			if($_POST["link"] != '') {
				
				#Look for the link or title already in the source table
				$sql = "select * from sources where sourceLink like '%" . $_POST["link"] . "%' or sourceTitle like '%" . $_POST["title"] . "%'";
				$result = $conn->query($sql);
				if($result->num_rows > 0) {
					echo "<br>Already some entries with info you entered.<br>";
					while($row = $result->fetch_assoc()) {
						echo "Source ID: " . $row["sourceID"] . "<br>Title: " . $row["sourceTitle"] . '<br>Link: ' . $row["sourceLink"] . "<br><br>";
					}
				} else {
					$sql = "insert into sources(sourceLink, sourceTitle)  values('" . $_POST["link"] . "', '" . $_POST["title"] . "')";
					echo $sql . "<br>";
					$result = $conn->query($sql);
				}
				
			}
		}
		
	}
}

if(isset($_POST["linky"])) {
	$sql = "select * from sources where sourceLink like '%" . $_POST["linky"]  . "%'";
	$result = $conn->query($sql);
	if($result->num_rows > 0) {
		echo "<br>Results for sources search:<br>";
		while($row = $result->fetch_assoc()) {
			echo "Source ID: " . $row["sourceID"] . "<br>Title: " . $row["sourceTitle"] . '<br>Link: ' . $row["sourceLink"] . "<br><br>";
		}
	} else {
		echo "<br>No results.<br>";
	}
}
?>
</html>
