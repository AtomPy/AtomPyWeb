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
?>

<html>
<a href='index.php'>Home</a><br>
<form action="addSources.php" method="post">
Title: <input type="text" name="title" size="100"><br>
Link: <input type="text" name="link" size="100"><br>
<input type="submit" value="Add Source">
</form>
</html>

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
				$sql = "select * from source where link like '%" . $_POST["link"] . "%' or title like '%" . $_POST["title"] . "%'";
				$result = $conn->query($sql);
				if($result->num_rows > 0) {
					echo "<br>Already some entries with info you entered.<br>";
					while($row = $result->fetch_assoc()) {
						echo $row["title"] . ', ' . $row["link"] . "<br>";
					}
				} else {
					$sql = "insert into source(link, title)  values('" . $_POST["link"] . "', '" . $_POST["title"] . "')";
					echo $sql . "<br>";
					$result = $conn->query($sql);
				}
				
			}
		}
		
	}
}

//Show the current sources
$sql = "select * from source";
$result = $conn->query($sql);
echo "<br>";
if($result->num_rows > 0) {
	while($row = $result->fetch_assoc()) {
		echo $row["id"] . "<br>" . $row["link"] . "<br>" . $row["title"] . "<br><br>";
	}
}

?>
