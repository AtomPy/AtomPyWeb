<?php
/* View File PHP Script for AtomPy 2.0
 * Created by Josiah Lucas Boswell (www.josiahboswell.com)
 * Takes queries and sends them to the python script.
 */
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

<?php
//Get our args
$Z = (string)$_POST["Z"];
$N = (string)$_POST["N"];
$SheetNum = (int)$_POST["SheetNum"];
$BackupArg = (string)$_POST["BackupArg"];

//Now get our file via our python download bot
$result = shell_exec("python WebAPI.py $Z $N $SheetNum $BackupArg 2>&1");

//Decode and print the result
$result = json_decode($result);
echo $result;

//Created by Josiah Lucas Boswell (www.josiahboswell.com)
?>