<?php
/* Logs File PHP Script for AtomPy 2.1
 *
 * Created by Josiah 'Lucas' Boswell (www.josiahboswell.com)
 *
 * Shows the last 10 entries of the upload log.
 */

//Extra debugging  for PHP errors
ini_set('display_errors',1);
error_reporting(E_ALL);
?>

<html>
<a href='index.php'>Home</a><br><br>

<?php

//Open up the log file and display
$handle = fopen("log.txt", "r");
if ($handle) {
    while (($line = fgets($handle)) !== false) {
        echo $line . "<br>";
    }
    fclose($handle);
} else {
    echo "Error opening log file.";
} 

?>
</html>