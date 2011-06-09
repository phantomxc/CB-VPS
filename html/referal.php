<?php
session_start()

$referrer = htmlspecialchars(mysql_real_escape_string($_GET[id]));

if ($referrer) {
    $expire = time()+60*60*24*30;

    if (isset($_COOKIE["referal"])) {
        Header("location:index.php");
    } else {
        setcookie("referal", $referrer, $expire);
        Header("location:index.php");
    }
} else {
    Header("location:index.php");
}


