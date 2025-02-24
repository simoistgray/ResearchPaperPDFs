import csv
import re


def extract_generic_name(college_name):
    patterns = [
        r'^(University of [A-Za-z\s]+)',  # Matches "University of ..."
        r'^(College of [A-Za-z\s]+)',  # Matches "College of ..."
        r'^(Institute of [A-Za-z\s]+)',  # Matches "Institute of ..."
    ]

    for pattern in patterns:
        match = re.match(pattern, college_name)
        if match:
            return match.group(1)
    return None


input_csv_path = 'world-universities.csv'
output_csv_path = 'updated-world-universities.csv'

existing_names = set()

with open(input_csv_path, 'r', newline='') as input_file:
    reader = csv.DictReader(input_file)
    for row in reader:
        existing_names.add(row['name'])

new_names = []

with open(input_csv_path, 'r', newline='') as input_file:
    reader = csv.DictReader(input_file)
    for row in reader:
        generic_name = extract_generic_name(row['name'])
        if generic_name and generic_name not in existing_names:
            new_names.append({'name': generic_name})
            existing_names.add(generic_name)

with open(output_csv_path, 'a', newline='') as output_file:
    fieldnames = ['name']
    writer = csv.DictWriter(output_file, fieldnames=fieldnames)

    if new_names:
        writer.writerows(new_names)

print("Generic college names have been added to the CSV file.")

