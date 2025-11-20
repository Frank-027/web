from flask import Flask, jsonify, request
import csv

app = Flask(__name__)

DATA_FILE = "p1_data_log.csv"
HOST_IP = "0.0.0.0"
PORT = 5001

def read_csv_records():
    records = []
    with open(DATA_FILE, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            records.append(row)
    return records

records = read_csv_records()
print(f"Loaded {len(records)} records from {DATA_FILE}")

# --- Bestaande route blijft voor random record ---
@app.route("/api/energy", methods=["GET"])
def get_random_record():
    import random
    if not records:
        return jsonify({"error": "Geen data beschikbaar"}), 500
    record = random.choice(records)
    return jsonify({
        "datetime": record["timestamp"],
        "active_power_w": float(record["active_power_w"]),
        "total_power_import_kwh": float(record["total_power_import_kwh"]),
        "total_power_export_kwh": float(record["total_power_export_kwh"]),
        "active_voltage_l1_v": float(record["active_voltage_l1_v"]),
        "active_current_a": float(record["active_current_a"]),
        "montly_power_peak_w": float(record["montly_power_peak_w"]),
        "montly_power_peak_timestamp": record["montly_power_peak_timestamp"]
    } )

# --- Nieuwe route: record opvragen per index ---
@app.route("/api/energy/<int:index>", methods=["GET"])
def get_record_by_index(index):
    if index < 0 or index >= len(records):
        return jsonify({"error": "Ongeldige index"}), 400

    record = records[index]
    return jsonify({
        "datetime": record["timestamp"],
        "active_power_w": float(record["active_power_w"]),
        "total_power_import_kwh": float(record["total_power_import_kwh"]),
        "total_power_export_kwh": float(record["total_power_export_kwh"]),
        "active_voltage_l1_v": float(record["active_voltage_l1_v"]),
        "active_current_a": float(record["active_current_a"]),
        "montly_power_peak_w": float(record["montly_power_peak_w"]),
        "montly_power_peak_timestamp": record["montly_power_peak_timestamp"]
    })

if __name__ == "__main__":
    print(f"Server gestart op http://{HOST_IP}:{PORT}/api/energy")
    app.run(host=HOST_IP, port=PORT)
