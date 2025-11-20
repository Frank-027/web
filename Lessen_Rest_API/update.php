<?php
$temp = $_POST['temp'];
$hum  = $_POST['hum'];

if ($temp !== null && $hum !== null) {
    $data = [
        "temperature" => floatval($temp),
        "humidity" => floatval($hum),
        "timestamp" => date("Y-m-d H:i:s")
    ];

    file_put_contents("data.json", json_encode($data, JSON_PRETTY_PRINT));
    echo "OK";
} else {
    echo "Invalid data";
}
?>
