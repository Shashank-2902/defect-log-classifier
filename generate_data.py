# generate_data.py
# Run this ONCE to create the two CSV files in the data/ folder.
# The logs are fully synthetic (made up) but written to look like real,
# messy automotive-semiconductor defect notes: mixed German/English, typos,
# inconsistent wording. This is what real quality logs actually look like.

import pandas as pd
from src import config

# Our single source of truth: each row is one made-up defect note, together
# with the correct category and severity that WE assign by hand.
# The format of each row is: (description, true_category, true_severity)
LOGS = [
    ("ultraschall sensor gibt keine daten, modul reagiert nicht", "Sensor Fault", "High"),
    ("CAN bus timeout, ECU no respond after 3 retries", "Communication Error", "High"),
    ("3.3v rail unstable, spannung schwankt stark am board", "Power Supply Issue", "High"),
    ("kalibrierung driftet seit firmware update leicht ab", "Calibration Drift", "Medium"),
    ("connector pin verbogen, gehaeuse hat riss", "Mechanical Damage", "Medium"),
    ("temp sensor liefert falsche werte, reading zu hoch", "Sensor Fault", "Medium"),
    ("lin bus kommunikation bricht ab bei kaelte", "Communication Error", "Medium"),
    ("power brownout beim start, board resettet", "Power Supply Issue", "High"),
    ("offset drift am drucksensor, muss neu kalibriert werden", "Calibration Drift", "Low"),
    ("platine verkratzt aber funktion ok", "Mechanical Damage", "Low"),
    ("radar modul kein signal, sensor tot", "Sensor Fault", "High"),
    ("spi communication error, checksum falsch", "Communication Error", "Medium"),
    ("voltage regulator ueberhitzt, 5v drops", "Power Supply Issue", "High"),
    ("messwerte langsam abweichend, drift ueber zeit", "Calibration Drift", "Medium"),
    ("stecker gebrochen beim einbau", "Mechanical Damage", "Medium"),
    ("hall sensor intermittierend, manchmal kein output", "Sensor Fault", "Medium"),
    ("ethernet link down sporadisch im fahrzeug", "Communication Error", "Medium"),
    ("kurzschluss auf power line vermutet", "Power Supply Issue", "High"),
    ("sensor zeigt konstant 0, wahrscheinlich defekt", "Sensor Fault", "High"),
    ("kalibrier offset zu gross nach transport", "Calibration Drift", "Low"),
    ("gehaeuse deformiert, aber elektronik laeuft", "Mechanical Damage", "Low"),
    ("i2c bus haengt, keine ack vom device", "Communication Error", "Medium"),
    ("board bekommt keine spannung, tot", "Power Supply Issue", "High"),
    ("light sensor ungenau bei sonnenlicht", "Sensor Fault", "Low"),
    ("firmware update failed, ecu nicht erreichbar", "Communication Error", "High"),
    ("kondensator ausgelaufen auf der platine", "Power Supply Issue", "Medium"),
    ("drift in messung nach temperaturwechsel", "Calibration Drift", "Medium"),
    ("pin header abgebrochen", "Mechanical Damage", "Medium"),
    ("proximity sensor rauscht stark", "Sensor Fault", "Low"),
    ("can frame verloren unter last", "Communication Error", "Medium"),
    ("netzteil liefert instabile spannung", "Power Supply Issue", "High"),
    ("sensor kalibrierung ausserhalb toleranz", "Calibration Drift", "Medium"),
    ("leiterbahn gerissen sichtbar", "Mechanical Damage", "High"),
    ("beschleunigungssensor liefert nan werte", "Sensor Fault", "High"),
    ("uart garbage data empfangen", "Communication Error", "Low"),
    ("spannungsspitze hat regler beschaedigt", "Power Supply Issue", "High"),
    ("langsamer drift am temperatur reading", "Calibration Drift", "Low"),
    ("schraube locker, modul wackelt", "Mechanical Damage", "Low"),
    ("magnetsensor kein signal mehr", "Sensor Fault", "High"),
    ("bus kollision auf can, viele fehler", "Communication Error", "Medium"),
    ("ground loop verursacht noise auf supply", "Power Supply Issue", "Medium"),
    ("kalibrierwerte verschoben nach reset", "Calibration Drift", "Medium"),
    ("stecker korrodiert, kontakt schlecht", "Mechanical Damage", "Medium"),
    ("feuchtigkeitssensor eingefroren wert", "Sensor Fault", "Medium"),
    ("modbus antwortet nicht mehr", "Communication Error", "Medium"),
    ("5v line noise ueber grenzwert", "Power Supply Issue", "Medium"),
    ("sensor genauigkeit nimmt langsam ab", "Calibration Drift", "Low"),
    ("gehaeuse gebrochen beim sturz", "Mechanical Damage", "High"),
    ("drucksensor liefert sprunghafte werte", "Sensor Fault", "Medium"),
    ("can bus komplett stumm nach start", "Communication Error", "High"),
    ("power supply schaltet nicht ein", "Power Supply Issue", "High"),
    ("kalibrierung langsam raus, offset waechst", "Calibration Drift", "Medium"),
    ("platinenkante abgebrochen", "Mechanical Damage", "Medium"),
    ("optischer sensor verschmutzt, keine daten", "Sensor Fault", "Low"),
    ("kommunikation instabil bei vibration", "Communication Error", "Medium"),
    ("spannung faellt unter 3v bei last", "Power Supply Issue", "High"),
    ("langzeit drift im gyroskop", "Calibration Drift", "Low"),
    ("mechanischer bruch am connector", "Mechanical Damage", "High"),
    ("sensor gibt sporadisch falsche id", "Sensor Fault", "Medium"),
    ("ecu verliert verbindung im standby", "Communication Error", "Medium"),
    ("board zieht zu viel strom, ueberlast", "Power Supply Issue", "High"),
    ("kalibrier routine schlaegt fehl", "Calibration Drift", "Medium"),
    ("kuehlkoerper lose, thermisch schlecht", "Mechanical Damage", "Low"),
    ("naeherungssensor reagiert verzoegert", "Sensor Fault", "Low"),
    ("crc fehler auf serieller schnittstelle", "Communication Error", "Medium"),
    ("regler liefert falsche ausgangsspannung", "Power Supply Issue", "Medium"),
    ("messgenauigkeit unter spezifikation", "Calibration Drift", "Medium"),
    ("steckverbinder gebrochen nach vibration", "Mechanical Damage", "Medium"),
    ("sensor uebertraegt nur nullen", "Sensor Fault", "High"),
    ("wlan modul verliert paket dauernd", "Communication Error", "Low"),
    # --- Ambiguous / hard rows: legitimately borderline cases. ---
    # These are meant to be difficult. The "true" label is the most
    # defensible single choice, but reasonable people could disagree.
    ("modul reagiert nicht nach firmware update", "Communication Error", "High"),
    ("werte springen nach kalibrierung, ursache unklar", "Calibration Drift", "Medium"),
    ("board verhaelt sich komisch seit einbau", "Mechanical Damage", "Low"),
    ("intermittierender fehler, mal sensor mal bus", "Communication Error", "Medium"),
    ("system instabil, koennte spannung oder software sein", "Power Supply Issue", "High"),
    ("modul liefert daten aber langsam und ungenau", "Sensor Fault", "Medium"),
    ("nach transport funktioniert etwas nicht richtig", "Mechanical Damage", "Medium"),
    ("sporadischer reset, grund nicht identifiziert", "Power Supply Issue", "High"),
    ("kommunikation ok aber messwerte driften leicht", "Calibration Drift", "Low"),
    ("gehaeuse ok aber sensor manchmal aus", "Sensor Fault", "Medium"),
    ("fehler tritt nur bei hitze auf, unklar was", "Calibration Drift", "Medium"),
    ("device antwortet verzoegert, timing problem", "Communication Error", "Low"),
]

def main():
    # Turn the list of tuples into a table (DataFrame) with named columns.
    df = pd.DataFrame(LOGS, columns=["description", "true_category", "true_severity"])

    # Give every row a simple id number: 1, 2, 3, ...
    # insert(0, ...) puts this new column at the very front.
    df.insert(0, "id", range(1, len(df) + 1))

    # raw_logs.csv = what the "system" would receive: just id + messy text.
    # No answers here. This is the input we will classify.
    df[["id", "description"]].to_csv(config.RAW_LOGS_PATH, index=False)

    # ground_truth.csv = our answer key: id + the correct category and severity.
    df[["id", "true_category", "true_severity"]].to_csv(config.GROUND_TRUTH_PATH, index=False)

    print(f"Wrote {len(df)} rows to {config.RAW_LOGS_PATH} and {config.GROUND_TRUTH_PATH}")

if __name__ == "__main__":
    main()