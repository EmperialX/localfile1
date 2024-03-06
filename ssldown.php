<?php

// Replace 'your_image_path' with the actual path to the image file on your server
$imagePath = 'your_image_path';

// Set the filename for the downloaded file
$filename = 'downloaded_picture.jpg';

// Set the MIME type for the file
$mime = mime_content_type($imagePath);

// Set appropriate headers for the response
header('Content-Type: ' . $mime);
header('Content-Disposition: attachment; filename="' . $filename . '"');

// Use OpenSSL to encrypt the file during download (optional)
// This is just a simple example, and you may need to adjust it based on your needs
$descriptorspec = [
    0 => ['pipe', 'r'], // stdin
    1 => ['pipe', 'w'], // stdout
    2 => ['pipe', 'w'], // stderr
];

$process = proc_open('openssl enc -aes-256-cbc -pass pass:your_password', $descriptorspec, $pipes);

if (is_resource($process)) {
    // Read the file content and encrypt it with OpenSSL
    $fileContent = file_get_contents($imagePath);
    fwrite($pipes[0], $fileContent);
    fclose($pipes[0]);

    // Read the encrypted content and send it to the client
    echo stream_get_contents($pipes[1]);

    // Close the process
    fclose($pipes[1]);
    fclose($pipes[2]);
    proc_close($process);
}

exit;
