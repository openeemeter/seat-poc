import random
import re
import csv
import numpy as np

regex = r"\(([\-0-9\.]+), ([\-0-9\.]+)\)"

output = []

N = 100000
samples = np.random.standard_cauchy(N) * 2 + 8 
samples_no_outliers = samples[(samples > -50) & (samples < 50)]
sample_index = 0

with open("assets/sf_buildings.csv") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        out = {}
        match = re.search(regex, row["Full.Address"])
        if match:
            lat = match.group(1)
            lng = match.group(2)

            out["lat"] = lat
            out["lng"] = lng
            out["ecm"] = random.choice([
                "Building Leakage",
                "HVAC System",
                "HVAC Duct Leakage",
                "Roof Insulation"
            ])
            out["building_type"] = random.choice([
                "Retail Store",
                "Office",
                "Hotel"
            ])
            
            out["savings"] = samples[sample_index]
            sample_index += 1

            output.append(out)

with open("assets/sf_buildings_clean.csv", "w") as outfile:
    writer = csv.DictWriter(outfile, fieldnames=[
        "lat",
        "lng",
        "ecm",
        "building_type",
        "savings"
    ])
    writer.writeheader()
    for row in output:
        writer.writerow(row)
