<?php
/* View File PHP Script for AtomPy 2.1
 *
 * Created by Josiah Lucas Boswell (www.josiahboswell.com)
 *
 * Takes queries and sends them to the python script.
 */
ini_set('display_errors',1);
error_reporting(E_ALL);
?>
<style>
table,th,td
{
border:1px solid black;
border-collapse:collapse;
padding:5px;
}
#right {
text-align: right;
}
#left {
text-align: left;
}
</style>
<a href="index.php">Home</a>
<?php
ini_set('display_errors',1);
error_reporting(E_ALL);

//Get our args
$Z = (string)$_POST["Z"];
$N = (string)$_POST["N"];
$SheetNum = (int)$_POST["SheetNum"];
$BackupArg = (string)$_POST["BackupArg"];

//Now get our file via our python download bot
echo date('Y-m-d H:i:s');
$result = shell_exec("python WebAPI.py $Z $N $SheetNum $BackupArg 2>&1");
echo date('Y-m-d H:i:s');
//Decode and print the result
$result = json_decode($result);
echo date('Y-m-d H:i:s');
echo $result;
echo date('Y-m-d H:i:s');

?>
