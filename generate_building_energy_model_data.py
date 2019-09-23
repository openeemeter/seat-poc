import csv
import random
from uszipcode import SearchEngine, Zipcode

search = SearchEngine(simple_zipcode=True)

with open("./processed_data/building_energy_model.csv", "w") as out:
    writer = csv.DictWriter(
        out,
        fieldnames=[
            "sqft",
            "floors",
            "lat",
            "lng",
            "year_built",
            "zipcode",
            "eui",
            "cvrmse",
            "nmbe",
        ],
    )

    writer.writeheader()
    with open("./assets/sf_buildings_clean.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            out = {}

            lat = float(row["lat"])
            lng = float(row["lng"])
            result = search.by_coordinates(lat, lng)
            out["lat"] = lat
            out["lng"] = lng
            out["zipcode"] = result[0].zipcode

            out["sqft"] = random.randint(1000, 30000)
            out["floors"] = random.randint(1, 15)
            out["year_built"] = random.randint(1900, 2000)

            out["eui"] = random.randint(0, 2000)
            out["cvrmse"] = random.randint(0, 10)
            out["nmbe"] = random.randint(0, 50)

            writer.writerow(out)
