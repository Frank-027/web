# -----------------------------------------------------------
# Energy Service API voor het kerstexamen 6ICW 2025
# Frank Demonie - Don Bosco Haacht  - December 2024
# -----------------------------------------------------------
from flask import Flask, jsonify, request
import csv
import random
import socket

app = Flask(__name__)

# -----------------------------------------------------------
# Lokaal IP-adres bepalen
# -----------------------------------------------------------
def get_local_ip():
    """Geeft het IP-adres van de Pi in het lokale netwerk terug"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Verbinding naar een extern adres, hoeft niet bereikbaar te zijn
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

LOCAL_IP = get_local_ip()

# -----------------------------------------------------------
# Bestanden
# -----------------------------------------------------------
TEST_FILE = "test_data.csv"
PROD_FILE = "production_data.csv"

HOST_IP = "0.0.0.0"
PORT = 5001

# -----------------------------------------------------------
# 1. API-keys met individuele indexen per dataset
# -----------------------------------------------------------
# API-keys per leerling (niet zomaar te raden)
VALID_API_KEYS = {
    "A1F3J8": {"test": 0, "prod": 0},
    "B7D2K1": {"test": 0, "prod": 0},
    "C9L4M5": {"test": 0, "prod": 0},
    "D3N6P7": {"test": 0, "prod": 0},
    "E2R8T9": {"test": 0, "prod": 0},
    "F4U1V3": {"test": 0, "prod": 0}
}

# Koppel de echte namen aan de API-key
STUDENT_NAMES = {
    "A1F3J8": "Max-Emile Boogaerts",
    "B7D2K1": "Noah Crabbé",
    "C9L4M5": "Mats Dumonceau",
    "D3N6P7": "Maarten Geets",
    "E2R8T9": "Dylan Lieser",
    "F4U1V3": "Kevin Verlinden"
}

ADMIN_KEY = "admin123"

# -----------------------------------------------------------
# 2. CSV inlezen
# -----------------------------------------------------------
def load_csv(filename):
    data = []
    with open(filename, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            data.append(row)
    return data

test_records = load_csv(TEST_FILE)
prod_records = load_csv(PROD_FILE)

print(f"Testdata geladen: {len(test_records)} records")
print(f"Productiedata geladen: {len(prod_records)} records")

# -----------------------------------------------------------
# 3. API-key validatie
# -----------------------------------------------------------
def check_api_key():
    key = request.args.get("apikey")

    if key is None:
        return None, jsonify({"error": "API-key ontbreekt"}), 401

    if key not in VALID_API_KEYS:
        return None, jsonify({"error": "Ongeldige API-key"}), 403

    return key, None, None

# -----------------------------------------------------------
# 4. Dataset validatie
# -----------------------------------------------------------
def get_dataset():
    dataset = request.args.get("dataset")
    if dataset not in ["test", "prod"]:
        return None, jsonify({"error": "dataset moet 'test' of 'prod' zijn"}), 400
    return dataset, None, None

def get_record_array(dataset):
    return test_records if dataset == "test" else prod_records

# -----------------------------------------------------------
# Route 1: Willekeurig record
# -----------------------------------------------------------
@app.route("/api/energy", methods=["GET"])
def get_random_record():

    key, err, status = check_api_key()
    if key is None:
        return err, status

    dataset, err, status = get_dataset()
    if dataset is None:
        return err, status

    records = get_record_array(dataset)
    record = random.choice(records)

    return jsonify(record)

# -----------------------------------------------------------
# Route 2: Volgend record (per leerling)
# -----------------------------------------------------------
@app.route("/api/energy/next", methods=["GET"])
def get_next_record():

    key, err, status = check_api_key()
    if key is None:
        return err, status

    dataset, err, status = get_dataset()
    if dataset is None:
        return err, status

    index = VALID_API_KEYS[key][dataset]
    records = get_record_array(dataset)

    if index >= len(records):
        return jsonify({"error": "Geen verdere records"}), 404

    record = records[index]

    VALID_API_KEYS[key][dataset] += 1

    return jsonify({
        "index": index,
        **record
    })

# -----------------------------------------------------------
# Route 3: Reset teller voor één student + dataset
# -----------------------------------------------------------
@app.route("/api/energy/reset", methods=["GET"])
def reset_index():

    key, err, status = check_api_key()
    if key is None:
        return err, status

    dataset, err, status = get_dataset()
    if dataset is None:
        return err, status

    VALID_API_KEYS[key][dataset] = 0

    return jsonify({
        "status": "OK",
        "message": f"Teller gereset voor '{dataset}'",
        "apikey": key
    })

# -----------------------------------------------------------
# Route 4: Status van teller
# -----------------------------------------------------------
@app.route("/api/energy/status", methods=["GET"])
def get_status():

    key, err, status = check_api_key()
    if key is None:
        return err, status

    dataset, err, status = get_dataset()
    if dataset is None:
        return err, status

    index = VALID_API_KEYS[key][dataset]
    total = len(get_record_array(dataset))

    return jsonify({
        "apikey": key,
        "dataset": dataset,
        "current_index": index,
        "total_records": total
    })

# -----------------------------------------------------------
# Route 5: Beschikbaar aantal records
# -----------------------------------------------------------
@app.route("/api/energy/max", methods=["GET"])
def max_records():
    return jsonify({
        "test_records": len(test_records),
        "prod_records": len(prod_records)
    })

# -----------------------------------------------------------
# Route 6: Reset ALL voor alle studenten (admin)
# -----------------------------------------------------------
@app.route("/api/energy/resetall", methods=["GET"])
def reset_all():

    key = request.args.get("apikey")

    if key != ADMIN_KEY:
        return jsonify({"error": "Geen toegang"}), 403

    for student in VALID_API_KEYS:
        VALID_API_KEYS[student]["test"] = 0
        VALID_API_KEYS[student]["prod"] = 0

    return jsonify({"status": "OK", "message": "Alle tellers gereset"})

# -----------------------------------------------------------
# Route 7: Uitgebreide API-help met extra info
# -----------------------------------------------------------
@app.route("/api/help", methods=["GET"])
def api_help():
    html = f"""
    <html>
    <head>
        <title>API Documentatie – Energy Service</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 40px;
                background-color: #f5f5f5;
                color: #333;
            }}
            h1, h2 {{
                color: #004080;
            }}
            code {{
                background-color: #eee;
                padding: 4px 6px;
                border-radius: 4px;
                font-size: 14px;
            }}
            .endpoint {{
                background: white;
                padding: 20px;
                margin-bottom: 20px;
                border-left: 6px solid #0078D4;
                border-radius: 6px;
            }}
            .example {{
                background: #fafafa;
                padding: 10px;
                border-radius: 4px;
                font-family: Consolas, monospace;
            }}
            .logo {{
                max-height: 100px;
                margin-bottom: 20px;
            }}
            .success {{
                background-color: #e0ffe0;
                padding: 15px;
                border-radius: 6px;
                margin-bottom: 30px;
                font-weight: bold;
            }}
        </style>
    </head>
    <body>

        <img src="/static/LogoDonBosco.png" alt="Don Bosco Haacht logo" class="logo">

        <h1>Energy API – Documentatie</h1>
        <p>Server IP: <b>{LOCAL_IP}</b> &nbsp;&nbsp; Poort: <b>{PORT}</b></p>

        <div class="success">
            Beste leerlingen, veel succes met jullie examen!!!
        </div>

        <p>Gebruik deze API's samen met jullie individuele API-key om testdata en productiedata record per record op te vragen.</p>

        <h2>Algemene parameters</h2>
        <ul>
            <li><b>apikey</b> – jouw persoonlijke API-sleutel</li>
            <li><b>dataset</b> – <code>test</code> of <code>prod</code></li>
        </ul>

        <hr>

        <div class="endpoint">
            <h2>1. Willekeurig record</h2>
            <p><code>GET /api/energy?dataset=&lt;test|prod&gt;&apikey=...</code></p>
            <p>Geeft een willekeurig record terug.</p>
            <div class="example">
                http://{LOCAL_IP}:{PORT}/api/energy?dataset=test&apikey=ABC123
            </div>
        </div>

        <div class="endpoint">
            <h2>2. Volgend record</h2>
            <p><code>GET /api/energy/next?dataset=&lt;test|prod&gt;&apikey=...</code></p>
            <p>Geeft het volgende record terug op basis van jouw teller.</p>
            <div class="example">
                http://{LOCAL_IP}:{PORT}/api/energy/next?dataset=prod&apikey=ABC123
            </div>
        </div>

        <div class="endpoint">
            <h2>3. Teller resetten (alleen voor jezelf)</h2>
            <p><code>GET /api/energy/reset?dataset=&lt;test|prod&gt;&apikey=...</code></p>
            <p>Zet de teller terug naar record 0.</p>
            <div class="example">
                http://{LOCAL_IP}:{PORT}/api/energy/reset?dataset=test&apikey=ABC123
            </div>
        </div>

        <div class="endpoint">
            <h2>4. Tellerstatus opvragen</h2>
            <p><code>GET /api/energy/status?dataset=&lt;test|prod&gt;&apikey=...</code></p>
            <p>Toont op welke recordindex je nu zit.</p>
            <div class="example">
                http://{LOCAL_IP}:{PORT}/api/energy/status?dataset=prod&apikey=ABC123
            </div>
        </div>

        <div class="endpoint">
            <h2>5. Maximum aantal records</h2>
            <p><code>GET /api/energy/max</code></p>
            <p>Geeft het totale aantal records in de CSV-bestanden.</p>
            <div class="example">
                http://{LOCAL_IP}:{PORT}/api/energy/max
            </div>
        </div>

        <div class="endpoint">
            <h2>6. Alle tellers resetten (alleen docent)</h2>
            <p><code>GET /api/energy/resetall?apikey=&lt;admin&gt;</code></p>
            <p>Reset alle tellers voor alle studenten.</p>
            <div class="example">
                http://{LOCAL_IP}:{PORT}/api/energy/resetall?apikey=???
            </div>
        </div>

        <hr>
        <p>Laat het weten als je nog iets niet begrijpt!</p>
        <p>Frank Demonie - Kerstexamen 6ICW 2025</p>

    </body>
    </html>
    """
    return html


# -----------------------------------------------------------
# Server start
# -----------------------------------------------------------
if __name__ == "__main__":
    print(f"Server gestart op http://{HOST_IP}:{PORT}/api/help")
    app.run(host=HOST_IP, port=PORT)
