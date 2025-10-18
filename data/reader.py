import csv
import os
from typing import Dict, List


def read_csv(file_path: str) -> List[Dict[str, str]]:
    """
    Reads a CSV file and returns its contents as a list of dictionaries.
    """
    try:
        with open(file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            return [row for row in reader]
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def get_movies_data() -> List[Dict[str, str]]:
    """
    Retrieves movie data from the predefined CSV file.
    """
    file_path = '/app/data/movies.csv'
    return read_csv(file_path)