import csv
import json


"""
Converts JSON data to CSV format and saves it to a CSV file.

This script loads data from a JSON file, converts it to CSV format, and saves 
it to a specified CSV file.
It includes column headers for 'title', 'rating', 'year', and 'poster_url'.

Usage:
    1. Ensure you have a valid 'data.json' file containing movie data in JSON 
    format.
    2. Specify the name of the CSV file ('movies.csv') where you want to save 
    the converted data.
    3. Run this script to perform the conversion and save the CSV file.

Note:
    - This script assumes that the JSON data structure is a dictionary where 
    keys are movie titles,
      and values are dictionaries containing 'rating', 'year', and 'poster_url'
       fields.
    - If any of these fields are missing in the JSON data, they will be 
    replaced with empty strings in the CSV.

Example:
    To convert 'data.json' to 'movies.csv', run the script as follows:
    $ python convert_json_to_csv.py

    After running the script, the CSV file 'movies.csv' will be created with 
    the converted data.

"""
# Load the JSON data
with open('data.json', 'r') as json_file:
    json_data = json.load(json_file)

# Define the CSV file name
csv_file = 'movies.csv'

# Write JSON data to CSV
with open(csv_file, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)

    # Write column headers
    csv_writer.writerow(['title', 'rating', 'year', 'poster_url'])

    # Write movie data
    for title, movie_data in json_data.items():
        rating = movie_data.get('rating', '')
        year = movie_data.get('year', '')
        poster_url = movie_data.get('poster_url', '')
        csv_writer.writerow([title, rating, year, poster_url])

print("CSV file 'movies.csv' created successfully.")
