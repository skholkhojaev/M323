import json
from datetime import datetime
from functools import reduce

def get_latest_date(data):
    """Finds the most recent date in the dataset."""
    return reduce(lambda latest, record: max(latest, record['jahr_monat']), data, "0000-00")

def get_last_n_months_from_latest(latest_year_month, n):
    """Returns a list of (year, month) strings for the last n months based on the most recent accident date."""
    latest_year, latest_month = map(int, latest_year_month.split('-'))
    
    def get_previous_month(year_month, _):
        year, month = year_month
        if month == 1:
            return year - 1, 12
        return year, month - 1
    
    months = [(latest_year, latest_month)]
    months.extend([get_previous_month(months[-1], _) for _ in range(n-1)])
    
    return [f"{year:04d}-{month:02d}" for year, month in months]

def filter_by_last_months(data, last_months):
    """Filters records by the last months."""
    return filter(lambda record: record['jahr_monat'] in last_months, data)

def group_by_municipality(data):
    """Groups records by municipality."""
    return reduce(lambda acc, record: {**acc, record['gemeinde']: acc.get(record['gemeinde'], []) + [record]}, data, {})

def list_latest_accidents_per_municipality(data):
    latest_year_month = get_latest_date(data)
    last_months = get_last_n_months_from_latest(latest_year_month, 2)
    
    accidents_per_municipality = group_by_municipality(filter_by_last_months(data, last_months))

    for municipality, records in accidents_per_municipality.items():
        print(f"Gemeinde {municipality}:")
        for record in records:
            print_record_info(record)

def accidents_in_municipality_last_n_years(data, selected_municipality, n_years):
    latest_year_month = get_latest_date(data)
    latest_year = int(latest_year_month.split('-')[0])
    years = [str(latest_year - i) for i in range(n_years)]
    
    filtered_accidents = filter(
        lambda record: record['jahr_monat'].split('-')[0] in years and record['gemeinde'] == selected_municipality, 
        data
    )
    
    accidents = list(filtered_accidents)
    
    if accidents:
        print(f"Unfälle in der Gemeinde {selected_municipality} in den letzten {n_years} Jahren:")
        for accident in accidents:
            print_record_info(accident)
    else:
        print(f"Keine Unfälle in der Gemeinde {selected_municipality} in den letzten {n_years} Jahren gefunden.")

def number_of_accidents_per_vehicle_type(data):
    vehicle_types = reduce(
        lambda acc, record: {**acc, record['fahrzeugart']: acc.get(record['fahrzeugart'], 0) + record['anzahl']}, 
        data, 
        {}
    )
    
    for vehicle_type, count in vehicle_types.items():
        print(f"{vehicle_type}: {count} Fahrzeuge")

def ranking_of_accidents_per_municipality(data):
    municipality_counts = reduce(
        lambda acc, record: {**acc, record['gemeinde']: acc.get(record['gemeinde'], 0) + record['anzahl']}, 
        data, 
        {}
    )

    sorted_municipalities = sorted(municipality_counts.items(), key=lambda x: x[1], reverse=True)
    print("Rangliste der Anzahl Fahrzeuge pro Gemeinde:")
    for rank, (municipality, count) in enumerate(sorted_municipalities, 1):
        print(f"{rank}. Gemeinde {municipality}: {count} Fahrzeuge")

def number_of_accidents_per_fuel_type(data):
    fuel_types = reduce(
        lambda acc, record: {**acc, (record['treibstoff'] or "Unbekannt"): acc.get(record['treibstoff'] or "Unbekannt", 0) + record['anzahl']}, 
        data, 
        {}
    )
    
    for fuel_type, count in fuel_types.items():
        print(f"{fuel_type}: {count} Fahrzeuge")

def print_record_info(record):
    print(f" Jahr-Monat: {record['jahr_monat']}")
    print(f" Gemeinde: {record['gemeinde']}")
    print(f" Fahrzeugart: {record['fahrzeugart']}")
    print(f" Treibstoff: {record['treibstoff'] or 'Unbekannt'}")
    print(f" Anzahl: {record['anzahl']}")
    print()

def main():
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
