import requests
import json
import time
import csv
from datetime import datetime

# --- CONFIG ---
P1_IP = "192.168.1.7"  # <-- vervang door IP van je HomeWizard P1
API_URL = f"http://{P1_IP}/api/v1/data"
OUTPUT_FILE = "p1_data_log.csv"

# --- Velden die we willen loggen ---
FIELDS = [
    "total_power_import_kwh",      # Totale stroomafname van het net (kWh)
    "total_power_export_kwh",      # Totale stroomteruglevering aan het net (kWh)
    "active_power_w",              # Huidig verbruik (W)
    "active_voltage_l1_v",         # Spanning op fase 1 (V)
    "active_current_a",            # Stroom op fase 1 (A)
    "active_power_average_w",      # Gemiddeld verbruik over korte periode (W)
    "montly_power_peak_w",         # Maandelijks piekverbruik (W)
    "montly_power_peak_timestamp", # Tijdstip van piekverbruik
    "total_gas_m3"                 # Totale gasafname (m³)
]

# --- CSV initialiseren ---
def init_csv(filename):
    with open(filename, "w", newline="") as f:
        # Eerste lijn = info/commentaar
        # f.write("# " + "; ".join([
        #    "timestamp: datum en tijd van meting (YYYY-MM-DD:HH:MM:SS)"
        # ] + [f"{field}: {FIELDS[field_index]}" if isinstance(FIELDS[field_index], str) else field
        #      for field_index, field in enumerate(FIELDS)]) + "\n")
        
        # Daarna de kolomtitels
        writer = csv.writer(f, delimiter=';')
        writer.writerow(["timestamp"] + FIELDS)
    print(f"[OK] CSV-bestand '{filename}' aangemaakt.\n")

# --- Data ophalen en loggen ---
def log_p1_data(duration, interval):
    start_time = time.time()
    n_records = 0

    while (time.time() - start_time) < duration:
        try:
            response = requests.get(API_URL, timeout=3)
            data = response.json()
            
            # Tijdstempel in gevraagd formaat
            timestamp = datetime.now().strftime("%Y-%m-%d:%H:%M:%S")
            row = [timestamp]
            
            # Velden toevoegen
            for field in FIELDS:
                value = data.get(field, None)

                # Specifieke omzetting van timestamp
                if field == "montly_power_peak_timestamp" and value is not None:
                    try:
                        value = datetime.strptime(str(value), "%y%m%d%H%M%S").strftime("%Y-%m-%d:%H:%M:%S")
                    except Exception as e:
                        print("⚠️ Kon timestamp niet converteren:", value, e)

                row.append(value)

            # Wegschrijven naar CSV
            with open(OUTPUT_FILE, "a", newline="") as f:
                writer = csv.writer(f, delimiter=';')
                writer.writerow(row)
            
            n_records += 1
            print(f"[{timestamp}] Record {n_records} gelogd.")

        except Exception as e:
            print("⚠️ Fout bij uitlezen:", e)
        
        time.sleep(interval)

    print(f"\n[KLAAR] Logging gestopt na {n_records} records ({duration} sec totaal).")

# --- MAIN ---
if __name__ == "__main__":
    try:
        duur = int(input("⏱️  Hoeveel seconden wil je data loggen? "))
        interval = float(input("⏲️  Interval tussen metingen (in seconden): "))
    except ValueError:
        print("❌ Ongeldige invoer. Gebruik een getal.")
        exit(1)

    print(f"\n➡️  Logging van {duur} seconden met interval {interval} sec naar '{OUTPUT_FILE}'...")
    print(f"➡️  P1-meter IP: {P1_IP}\n")

    init_csv(OUTPUT_FILE)
    log_p1_data(duur, interval)