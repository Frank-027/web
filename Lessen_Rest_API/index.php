<?php
// Bestand waarin we de huidige status bewaren
$statusFile = 'status.json';

// Initieer standaardstatus (indien nog niet bestaat)
if (!file_exists($statusFile)) {
    file_put_contents($statusFile, json_encode(['led1' => 0, 'led2' => 0]));
}

// Lees huidige status
$status = json_decode(file_get_contents($statusFile), true);

// Controleer of er een actie werd doorgestuurd
if (isset($_GET['led']) && isset($_GET['state'])) {
    $led = $_GET['led'];
    $state = $_GET['state'] == '1' ? 1 : 0;
    $status[$led] = $state;
    file_put_contents($statusFile, json_encode($status));
}

// HTML output
?>
<!DOCTYPE html>
<html>
<head>
    <title>ESP32 LED Control</title>
    <style>
        body { font-family: Arial; text-align: center; margin-top: 50px; }
        button { font-size: 20px; margin: 10px; padding: 10px 20px; }
        .on  { background: limegreen; }
        .off { background: lightgray; }
    </style>
</head>
<body>
    <h1>ESP32 LED Control</h1>
    <p>LED 1 is <?= $status['led1'] ? 'ON' : 'OFF' ?></p>
    <a href="?led=led1&state=<?= $status['led1'] ? 0 : 1 ?>">
        <button class="<?= $status['led1'] ? 'on' : 'off' ?>">
            Zet LED 1 <?= $status['led1'] ? 'UIT' : 'AAN' ?>
        </button>
    </a>
    <p>LED 2 is <?= $status['led2'] ? 'ON' : 'OFF' ?></p>
    <a href="?led=led2&state=<?= $status['led2'] ? 0 : 1 ?>">
        <button class="<?= $status['led2'] ? 'on' : 'off' ?>">
            Zet LED 2 <?= $status['led2'] ? 'UIT' : 'AAN' ?>
        </button>
    </a>
</body>
</html>
