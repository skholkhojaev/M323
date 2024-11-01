"""
Dieses Programm analysiert Verkehrsunfalldaten aus einer JSON-Datei und bietet mehrere Optionen zur Anzeige und Auswertung:
1. Liste der neuesten Unfälle (letzte 2 Monate) pro Gemeinde
2. Unfälle einer bestimmten Gemeinde in den letzten 2 Jahren
3. Anzahl der Unfälle nach Fahrzeugtyp
4. Rangliste der Unfallanzahl pro Gemeinde
5. Anzahl der Unfälle nach Treibstoffart

Autor: Sino, Janie
Version: 1.0
"""

import json
from datetime import datetime

def get_latest_date(data):
    """
    Ermittelt das neueste Jahr-Monat-Datum in den Daten.

    Parameter:
    data (list): Liste der Unfallaufzeichnungen

    Rückgabewert:
    str: Das neueste Jahr-Monat-Datum im Format 'YYYY-MM'
    """
    latest_year_month = "0000-00"
    for record in data:
        if record['jahr_monat'] > latest_year_month:
            latest_year_month = record['jahr_monat']
    return latest_year_month

def get_last_n_months_from_latest(latest_year_month, n):
    """
    Erstellt eine Liste der letzten 'n' Monate ab einem gegebenen Jahr-Monat-Wert.

    Parameter:
    latest_year_month (str): Das neueste Datum im Format 'YYYY-MM'
    n (int): Anzahl der Monate

    Rückgabewert:
    list: Liste der letzten 'n' Monate im Format 'YYYY-MM'
    """
    latest_year, latest_month = map(int, latest_year_month.split('-'))
    months = []
    year, month = latest_year, latest_month
    for _ in range(n):
        months.append(f"{year:04d}-{month:02d}")
        if month == 1:
            year -= 1
            month = 12
        else:
            month -= 1
    return months

def list_latest_accidents_per_municipality(data):
    """
    Listet die neuesten Unfallaufzeichnungen der letzten 2 Monate nach Gemeinde auf.

    Parameter:
    data (list): Liste der Unfallaufzeichnungen
    """
    latest_year_month = get_latest_date(data)
    last_months = get_last_n_months_from_latest(latest_year_month, 2)
    accidents_per_municipality = {}

    for record in data:
        if record['jahr_monat'] in last_months:
            municipality = record['gemeinde']
            if municipality not in accidents_per_municipality:
                accidents_per_municipality[municipality] = []
            accidents_per_municipality[municipality].append(record)
    
    for municipality, records in accidents_per_municipality.items():
        print(f"Gemeinde {municipality}:")
        for record in records:
            print_record_info(record)

def accidents_in_municipality_last_n_years(data, selected_municipality, n_years):
    """
    Listet Unfälle einer bestimmten Gemeinde in den letzten 'n' Jahren auf.

    Parameter:
    data (list): Liste der Unfallaufzeichnungen
    selected_municipality (str): Name der ausgewählten Gemeinde
    n_years (int): Anzahl der Jahre für die Rückwärtssuche
    """
    latest_year_month = get_latest_date(data)
    latest_year, _ = map(int, latest_year_month.split('-'))
    years = [str(latest_year - i) for i in range(n_years)]
    accidents = []

    for record in data:
        year = record['jahr_monat'].split('-')[0]
        if year in years and record['gemeinde'] == selected_municipality:
            accidents.append(record)

    if accidents:
        print(f"Unfälle in der Gemeinde {selected_municipality} in den letzten {n_years} Jahren:")
        for accident in accidents:
            print_record_info(accident)
    else:
        print(f"Keine Unfälle in der Gemeinde {selected_municipality} in den letzten {n_years} Jahren gefunden.")

def number_of_accidents_per_vehicle_type(data):
    """
    Gibt die Anzahl der Unfälle pro Fahrzeugtyp aus.

    Parameter:
    data (list): Liste der Unfallaufzeichnungen
    """
    vehicle_types = {}
    for record in data:
        vehicle_type = record['fahrzeugart']
        vehicle_types[vehicle_type] = vehicle_types.get(vehicle_type, 0) + record['anzahl']
    
    for vehicle_type, count in vehicle_types.items():
        print(f"{vehicle_type}: {count} Fahrzeuge")

def ranking_of_accidents_per_municipality(data):
    """
    Erstellt eine Rangliste der Anzahl der Unfälle pro Gemeinde.

    Parameter:
    data (list): Liste der Unfallaufzeichnungen
    """
    municipality_counts = {}
    for record in data:
        municipality = record['gemeinde']
        municipality_counts[municipality] = municipality_counts.get(municipality, 0) + record['anzahl']

    sorted_municipalities = sorted(municipality_counts.items(), key=lambda x: x[1], reverse=True)
    print("Rangliste der Anzahl Fahrzeuge pro Gemeinde:")
    for rank, (municipality, count) in enumerate(sorted_municipalities, 1):
        print(f"{rank}. Gemeinde {municipality}: {count} Fahrzeuge")

def number_of_accidents_per_fuel_type(data):
    """
    Gibt die Anzahl der Unfälle pro Treibstoffart aus.

    Parameter:
    data (list): Liste der Unfallaufzeichnungen
    """
    fuel_types = {}
    for record in data:
        fuel_type = record['treibstoff'] or "Unbekannt"
        fuel_types[fuel_type] = fuel_types.get(fuel_type, 0) + record['anzahl']
    
    for fuel_type, count in fuel_types.items():
        print(f"{fuel_type}: {count} Fahrzeuge")

def print_record_info(record):
    """
    Gibt detaillierte Informationen einer Unfallaufzeichnung aus.

    Parameter:
    record (dict): Eine Unfallaufzeichnung
    """
    print(f" Jahr-Monat: {record['jahr_monat']}")
    print(f" Gemeinde: {record['gemeinde']}")
    print(f" Fahrzeugart: {record['fahrzeugart']}")
    print(f" Treibstoff: {record['treibstoff'] or 'Unbekannt'}")
    print(f" Anzahl: {record['anzahl']}")
    print()

def main():
    """
    Hauptprogramm, lädt die Daten und bietet dem Benutzer verschiedene Optionen zur Auswahl.
    """
    try:
        with open('roadtrafficaccidentlocations.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Die Datei 'roadtrafficaccidentlocations.json' wurde nicht gefunden.")
        return
    except json.JSONDecodeError:
        print("Fehler beim Lesen der JSON-Datei.")
        return

    while True:
        print("\nBitte wählen Sie eine Funktion aus:")
        print("1. Liste der neusten Fahrzeuge (letzte 2 Monate) pro Gemeinde")
        print("2. Die Fahrzeuge einer ausgewählten Gemeinde in den letzten 2 Jahren")
        print("3. Gibt die Anzahl der Fahrzeuge pro Fahrzeugart aus")
        print("4. Rangliste der Anzahl Fahrzeuge pro Gemeinde")
        print("5. Anzahl der Fahrzeuge pro Treibstoffart")
        print("6. Beenden")
        choice = input("Ihre Wahl (1-6): ")

        if choice == '1':
            list_latest_accidents_per_municipality(data)
        elif choice == '2':
            selected_municipality = input("Bitte geben Sie den Gemeindenamen ein (z.B., 'Grellingen'): ")
            accidents_in_municipality_last_n_years(data, selected_municipality, 2)
        elif choice == '3':
            number_of_accidents_per_vehicle_type(data)
        elif choice == '4':
            ranking_of_accidents_per_municipality(data)
        elif choice == '5':
            number_of_accidents_per_fuel_type(data)
        elif choice == '6':
            print("Programm beendet.")
            break
        else:
            print("Ungültige Auswahl. Bitte versuchen Sie es erneut.")

if __name__ == "__main__":
    main()
