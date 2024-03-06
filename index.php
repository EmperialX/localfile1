<?php
if (!empty($_SERVER['HTTPS']) && ('on' == $_SERVER['HTTPS'])) {
    $uri = 'https://';
} else {
    $uri = 'http://';
}
$uri .= $_SERVER['HTTP_HOST'];

// Add the comment with the flag here
$flag_comment = "HTB{flag_flag}";
header('Location: '.$uri.'/xampp/'); // Redirect to /xampp/
exit;
?>
