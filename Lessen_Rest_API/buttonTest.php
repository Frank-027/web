<?php
// Bestand waarin we de huidige status bewaren
$statusFile = 'status.json';
if (!file_exists($statusFile)) {
    file_put_contents($statusFile, json_encode(['led1' => 0, 'led2' => 0]));
}
$status = json_decode(file_get_contents($statusFile), true);

// Wanneer een slider verandert (GET-request)
if (isset($_GET['led']) && isset($_GET['state'])) {
    $led = $_GET['led'];
    $state = $_GET['state'] == '1' ? 1 : 0;
    $status[$led] = $state;
    file_put_contents($statusFile, json_encode($status));
}
?>
<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ESP32 LED Control</title>
<style>
    body {
        font-family: 'Segoe UI', Arial, sans-serif;
        background: #f5f7fa;
        color: #222;
        text-align: center;
        padding-top: 50px;
    }
    h1 { color: #333; }

    .switch-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 20px auto;
        width: 300px;
        padding: 20px;
        background: white;
        border-radius: 15px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }

    .switch-label {
        flex: 1;
        text-align: left;
        font-size: 18px;
    }

    .switch {
        position: relative;
        display: inline-block;
        width: 60px;
        height: 34px;
    }
    .switch input { display: none; }

    .slider {
        position: absolute;
        cursor: pointer;
        top: 0; left: 0;
        right: 0; bottom: 0;
        background-color: #ccc;
        transition: 0.4s;
        border-radius: 34px;
    }

    .slider:before {
        position: absolute;
        content: "";
        height: 26px;
        width: 26px;
        left: 4px;
        bottom: 4px;
        background-color: white;
        transition: 0.4s;
        border-radius: 50%;
    }

    input:checked + .slider {
        background-color: #4CAF50;
    }

    input:checked + .slider:before {
        transform: translateX(26px);
    }

    footer {
        margin-top: 40px;
        font-size: 12px;
        color: #777;
    }
</style>
<script>
function toggleLED(led, checkbox) {
    const state = checkbox.checked ? 1 : 0;
    fetch(`?led=${led}&state=${state}`)
      .then(() => console.log(`LED ${led} => ${state}`));
}
</script>
</head>
<body>

<h1>ESP32 LED Control Panel</h1>

<div class="switch-container">
    <span class="switch-label">LED 1</span>
    <label class="switch">
        <input type="checkbox" onchange="toggleLED('led1', this)" <?= $status['led1'] ? 'checked' : '' ?>>
        <span class="slider"></span>
    </label>
</div>

<div class="switch-container">
    <span class="switch-label">LED 2</span>
    <label class="switch">
        <input type="checkbox" onchange="toggleLED('led2', this)" <?= $status['led2'] ? 'checked' : '' ?>>
        <span class="slider"></span>
    </label>
</div>

<footer>
    Raspberry Pi – ESP32 HTTP Control © 2025
</footer>

</body>
</html>