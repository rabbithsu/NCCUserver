<?php
$db = mysqli_connect("localhost","root","","Stock");

mysqli_query($db, "SET CHARACTER SET 'UTF8';");
mysqli_query($db, 'SET NAMES UTF8;');
mysqli_query($db, 'SET CHARACTER_SET_CLIENT=UTF8;');
mysqli_query($db, 'SET CHARACTER_SET_RESULTS=UTF8;');


$sql = $_POST['query_string'];
$sql = stripslashes($sql);
/*$sql = "SELECT result FROM predict ORDER BY date desc, id asc";*/

if ($result = mysqli_query($db, $sql)) {

    /* fetch associative array */
    while ($row = mysqli_fetch_assoc($result)) {
        $output[] = $row;
    }
    print(json_encode($output));

    /* free result set */
    mysqli_free_result($result);
}

/* close connection */
mysqli_close($db);

?>
