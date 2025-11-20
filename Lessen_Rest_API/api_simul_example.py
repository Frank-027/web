from flask import Flask, jsonify
import csv

app = Flask(__name__)

DATA_FILE = "test_data.csv"
HOST_IP = "0.0.0.0"
PORT = 5000

def read_csv_records():
    records = []
    with open(DATA_FILE, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            records.append(row)
    return records

records = read_csv_records()
print(f"Loaded {len(records)} records from {DATA_FILE}")

@app.route("/api/data/<int:index>", methods=["GET"])
def get_record_by_index(index):
    if index < 0 or index >= len(records):
        return jsonify({"error": "Ongeldige index"}), 400

    record = records[index]
    return jsonify({
        "timestamp": record["timestamp"],
        "temperature_c": float(record["temperature_c"]),
        "humidity_pct": float(record["humidity_pct"]),
        "light_level": float(record["light_level"]),
        "co2_ppm": float(record["co2_ppm"])
    })

if __name__ == "__main__":
    print(f"Server gestart op http://{HOST_IP}:{PORT}/api/data/<index>")
    app.run(host=HOST_IP, port=PORT)
