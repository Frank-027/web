<?php
// Debug-informatie
error_reporting(E_ALL);
ini_set('display_errors', 1);

// Ontvangen POST-data
$temp = isset($_POST['temp']) ? $_POST['temp'] : null;
$hum  = isset($_POST['hum']) ? $_POST['hum'] : null;

echo "<pre>";  // overzichtelijke weergave

echo "Ontvangen POST-data:\n";
print_r($_POST);

if ($temp !== null && $hum !== null) {
    echo "\nData aanwezig. Proberen te schrijven naar data.json...\n";

    $data = [
        "temperature" => floatval($temp),
        "humidity"    => floatval($hum),
        "timestamp"   => date("Y-m-d H:i:s")
    ];

    $json = json_encode($data, JSON_PRETTY_PRINT);

    $result = file_put_contents("data.json", $json);

    if ($result !== false) {
        echo "data.json succesvol aangemaakt!\n";
    } else {
        echo "Fout bij aanmaken data.json! Controleer bestandsrechten.\n";
    }

    echo "\nInhoud JSON:\n";
    echo $json;
} else {
    echo "POST-data niet correct ontvangen.\n";
}

echo "</pre>";
?>
