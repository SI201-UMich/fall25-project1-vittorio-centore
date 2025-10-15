### SI 201 Project 1: CSV
### Name: Jackson Miller
### Uniqname: miljack
### UMID: 7012 3312
### Collaborators: Vittorio Centore and ChatGPT 5.0 and Gemini Pro
### Gen AI Statement: Used ChatGPT for general potential function outlines for inputs, outputs, and usage,
### , and for our flowchart ideas. We used Gemini and ChatGPT collectively for general debugging help.

import csv
import unittest
import math

def load_data(csv_file: str):
    """
    This is a combined function that both imports the csv file 
    and creates a dictionary for each line
    using try except since we are reading in files 
    """
    data = []
    with open(csv_file, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:

            ## reading in each row for our columns. While the columns below may not be our
            ## selected ones, we have to read them in correctly or they return none
            ## so we read in by float or int depending on context
            ## Using try except because of file opening risk 
            if row.get("bill_length_mm"):
                try:
                    row["bill_length_mm"] = float(row["bill_length_mm"])
                except ValueError:
                    row["bill_length_mm"] = None

            if row.get("bill_depth_mm"):
                try:
                    row["bill_depth_mm"] = float(row["bill_depth_mm"])
                except ValueError:
                    row["bill_depth_mm"] = None

            if row.get("flipper_length_mm"):
                try:
                    row["flipper_length_mm"] = int(row["flipper_length_mm"])
                except ValueError:
                    row["flipper_length_mm"] = None

            if row.get("body_mass_g"):
                try:
                    row["body_mass_g"] = int(row["body_mass_g"])
                except ValueError:
                    row["body_mass_g"] = None

            ### For rows that don't need int or float conversion, just append 
            data.append(row)
    return data


def calculate_average_body_mass(data):
    """
    Calculates average body mass for each penguin species.
    INPUT: data (list of dicts)
    OUTPUT: avg_body_mass (dict {species: avg_mass})
    """

    avg_body_mass = {}
    for row in data:
        row_species = row.get("species")
        row_mass = row.get("body_mass_g")
        flipper = row.get("flipper_length_mm")
        if row_mass is None or flipper is None:
            # changed from setting to zero to skipping to avoid skewing
            continue

        ## Using dict to store mass for each species 
        if row_species not in avg_body_mass:
            avg_body_mass[row_species] = {"total_mass": 0, "count": 0}

        avg_body_mass[row_species]["total_mass"] += row_mass
        avg_body_mass[row_species]["count"] += 1 

    for species, values in avg_body_mass.items():
        if values["count"] > 0:
            avg_body_mass[species] = values["total_mass"] / values["count"]
        else:
            avg_body_mass[species] = 0

    print(">>> Avg body mass with valid flipper data:", avg_body_mass)
    return avg_body_mass


def select_heavy_bills(data):
    """
    Filters penguins with body mass > 3500g 
    and calculates average bill length.
    INPUT: data (list of dicts)
    OUTPUT: avg_bill_length (float)
    """

    # filters penguins above 3500g and a minimum bill depth of 17.0mm
    heavy_bills = [p for p in data 
                   if p.get("body_mass_g") and p["body_mass_g"] > 3500 
                   and p.get("bill_length_mm") and p.get("bill_depth_mm") and p["bill_depth_mm"] >= 17.0]

    if heavy_bills:
        avg_bill_length = sum(p["bill_length_mm"] for p in heavy_bills) / len(heavy_bills)
    else:
        avg_bill_length = 0  # handle no heavy bills

    print(f">>> Avg bill length for body mass > 3500g and above the minimum bill depth of 17.0mm: {avg_bill_length:.3f} mm")
    return avg_bill_length


def find_upper_quartile_long_bills(data):
    valid_masses = [p["body_mass_g"] for p in data if p.get("body_mass_g")]
    if not valid_masses:
        return 0

    valid_masses.sort()
    # Use floor to include 75th percentile and above
    index_75 = math.floor(0.75 * len(valid_masses)) - 1
    if index_75 < 0:
        index_75 = 0
    upper_cutoff = valid_masses[index_75]

    long_bills = [
        p for p in data
        if p.get("body_mass_g") and p["body_mass_g"] >= upper_cutoff
        and p.get("bill_length_mm") and p["bill_length_mm"] > 42
    ]

    count = len(long_bills)
    print(f">>> Penguins in top 25% body mass AND bill length > 42mm: {count}")
    return count



def find_heavy_quartile_long_bills(data):
    """
    Counts penguins with body mass > 4000g.
    INPUT: data (list of dicts)
    OUTPUT: count (int)
    """

    # filters based on minimum mass threshold
    heavy_penguins = [p for p in data if p.get("body_mass_g") and p["body_mass_g"] > 4000]

    count = len(heavy_penguins)

    print(f">>> Total penguins with body mass > 4000g: {count}")
    return count


def find_heavy_gentoo_count(data):
    """
    Counts total Gentoo penguins with body mass > 4000g.
    INPUT: data (list of dicts)
    OUTPUT: count (int)
    """

    gentoo_heavy = [p for p in data 
                    if p.get("species") == "Gentoo" 
                    and p.get("body_mass_g") 
                    and p["body_mass_g"] > 4000]

    count = len(gentoo_heavy)

    print(f">>> Total Gentoo penguins with body mass > 4000g: {count}")
    return count


class test_work(unittest.TestCase):
    def test_load_data(self):
        data = load_data("project/penguins.csv")
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)
        self.assertIsInstance(data[0], dict)
        self.assertEqual(set(data[0].keys()), {'', 'species', 'island', 'bill_length_mm', 'bill_depth_mm', 'flipper_length_mm', 'body_mass_g', 'sex', 'year'})

    def test_calculate_average_body_mass(self):
        data = [
            {"species": "Adelie", "body_mass_g": 3700, "flipper_length_mm": 190},
            {"species": "Adelie", "body_mass_g": 3800, "flipper_length_mm": 195},
            {"species": "Chinstrap", "body_mass_g": 3500, "flipper_length_mm": 200},
            {"species": "Chinstrap", "body_mass_g": None, 'flipper_length_mm': 198},
            {"species": "Gentoo", "body_mass_g": 5000, "flipper_length_mm": 210}
        ]
        avg_body_mass = calculate_average_body_mass(data)
        self.assertAlmostEqual(avg_body_mass["Adelie"], 3750.0)
        self.assertAlmostEqual(avg_body_mass["Chinstrap"], 3500.0)
        self.assertAlmostEqual(avg_body_mass["Gentoo"], 5000.0)

    def test_select_heavy_bills(self):
        data = [
            {"body_mass_g": 3600, "bill_length_mm": 40, "bill_depth_mm": 18.0},
            {"body_mass_g": 3700, "bill_length_mm": 42, "bill_depth_mm": 17.5},
            {"body_mass_g": 3400, "bill_length_mm": 39, "bill_depth_mm": 16.0},
            {"body_mass_g": None, "bill_length_mm": 41, "bill_depth_mm": 19.0},
        ]
        avg_bill_length = select_heavy_bills(data)
        self.assertAlmostEqual(avg_bill_length, 41.0)

    def test_find_upper_quartile_long_bills(self):
        data = [
            {"body_mass_g": 3000, "bill_length_mm": 40},
            {"body_mass_g": 3600, "bill_length_mm": 43},
            {"body_mass_g": 4200, "bill_length_mm": 44},
            {"body_mass_g": 4600, "bill_length_mm": 41},
            {"body_mass_g": 4800, "bill_length_mm": 45}
        ]
        result = find_upper_quartile_long_bills(data)
        self.assertEqual(result, 2)  # top 25% mass + bill length > 42

    def test_find_heavy_quartile_long_bills(self):
        data = [
            {"body_mass_g": 3900},
            {"body_mass_g": 4100},
            {"body_mass_g": 4500},
            {"body_mass_g": None},
        ]
        result = find_heavy_quartile_long_bills(data)
        self.assertEqual(result, 2)  # two above 4000

    def test_find_heavy_gentoo_count(self):
        data = [
            {"species": "Gentoo", "body_mass_g": 4100},
            {"species": "Gentoo", "body_mass_g": 3900},
            {"species": "Adelie", "body_mass_g": 4500},
            {"species": "Gentoo", "body_mass_g": 4200},
        ]
        result = find_heavy_gentoo_count(data)
        self.assertEqual(result, 2)  # only two Gentoo above 4000


def main():
    """
    Calls the other functions in a logical sequence.
    INPUT: None
    OUTPUT: None
    """

    file_path = "project/penguins.csv"

    # Confirms the file path is correct          
    print(">>> Looking for:", file_path)    
    
    csv_data = load_data(file_path)

    # confirming csv_data produces desired output 
    print(">>> Rows loaded:", len(csv_data))
    for row in csv_data:
        print(row)

    # run calculations
    calculate_average_body_mass(csv_data)
    select_heavy_bills(csv_data)
    find_upper_quartile_long_bills(csv_data)
    find_heavy_quartile_long_bills(csv_data)
    find_heavy_gentoo_count(csv_data)


if __name__ == "__main__":
    main()  # optional: runs your main function
    unittest.main()
