import pandas as pd

def convert_embedding_data_to_csv():
    """
    Converts a JSON file to a CSV file.

    Parameters:
    json_file_path (str): The path to the input JSON file.
    csv_file_path (str): The path to the output CSV file.
    """
    # Read the JSON file into a DataFrame
    menu_path = '/app/data/default.tasks.menu'
    search_path = '/app/data/default.tasks.search'
    df_menu = pd.read_json(menu_path)
    df_search = pd.read_json(search_path)
    print(df_menu.head())
    print(df_search.head())