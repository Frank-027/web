<?php
// buttonTest.php
$statusFile = __DIR__ . '/status.json';

// Zorg dat status.json bestaat
if (!file_exists($statusFile)) {
    file_put_contents($statusFile, json_encode(['led1'=>0,'led2'=>0]));
}

// Lees huidige status
$status = json_decode(file_get_contents($statusFile), true);

// Update via POST
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $input = json_decode(file_get_contents("php://input"), true);
    if (isset($input['led1'])) $status['led1'] = $input['led1'] ? 1 : 0;
    if (isset($input['led2'])) $status['led2'] = $input['led2'] ? 1 : 0;
    file_put_contents($statusFile, json_encode($status));
    header('Content-Type: application/json');
    echo json_encode(['success'=>true,'status'=>$status]);
    exit;
}

// Live status ophalen via GET
if (isset($_GET['getStatus'])) {
    header('Content-Type: application/json');
    echo json_encode($status);
    exit;
}
?>
<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="UTF-8">
<title>ESP32 LED Control POST</title>
<style>
body { font-family: Arial; text-align:center; margin-top:50px; background:#f0f0f0; }
.switch { position: relative; display: inline-block; width:60px; height:34px; }
.switch input {display:none;}
.slider { position: absolute; cursor:pointer; top:0; left:0; right:0; bottom:0; background:#ccc; border-radius:34px; transition:.4s; }
.slider:before { position:absolute; content:""; height:26px; width:26px; left:4px; bottom:4px; background:white; border-radius:50%; transition:.4s; }
input:checked + .slider { background:#4CAF50; }
input:checked + .slider:before { transform:translateX(26px); }
.container { background:white; padding:20px; margin:20px auto; width:250px; border-radius:10px; box-shadow:0 2px 6px rgba(0,0,0,.2); }
</style>
<script>
// Verstuur LED-status via POST
function postLED(led, checkbox) {
    const state = checkbox.checked ? 1 : 0;
    fetch('buttonTest.php', {
        method:'POST',
        headers:{'Content-Type':'application/json'},
        body: JSON.stringify({[led]: state})
    });
}

// Live update sliders elke 1s
function updateStatus() {
    fetch('buttonTest.php?getStatus')
    .then(resp=>resp.json())
    .then(data=>{
        document.getElementById('led1').checked = data.led1==1;
        document.getElementById('led2').checked = data.led2==1;
    });
}
setInterval(updateStatus,1000);
</script>
</head>
<body>
<h2>ESP32 LED Control POST (Live)</h2>

<div class="container">
LED 1
<label class="switch">
<input type="checkbox" id="led1" onchange="postLED('led1',this)">
<span class="slider"></span>
</label>
</div>

<div class="container">
LED 2
<label class="switch">
<input type="checkbox" id="led2" onchange="postLED('led2',this)">
<span class="slider"></span>
</label>
</div>

</body>
</html>
