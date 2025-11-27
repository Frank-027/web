from flask import Flask, jsonify
import csv

app = Flask(__name__)

DATA_FILE = "punten.csv"
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

@app.route("/api/data/<int:index>", methods=["GET"])
def get_record_by_index(index):
    if index < 0 or index >= len(records):
        return jsonify({"error": "Ongeldige index"}), 400

    record = records[index]
    return jsonify({
        "student_id": int(record["student_id"]),
        "naam": record["naam"],
        "wiskunde": int(record["wiskunde"]),
        "fysica": int(record["fysica"]),
        "informatica": int(record["informatica"]),
        "mechanica": int(record["mechanica"]),
        "elektronica": int(record["elektronica"]),
        "engels": int(record["engels"]),
        "nederlands": int(record["nederlands"]),
        "geschiedenis": int(record["geschiedenis"]),
        "aardrijkskunde": int(record["aardrijkskunde"])
    })

if __name__ == "__main__":
    print(f"Server gestart op http://{HOST_IP}:{PORT}/api/data/<index>")
    app.run(host=HOST_IP, port=PORT)