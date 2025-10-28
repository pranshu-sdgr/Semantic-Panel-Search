import pandas as pd
import os

def to_csv():
    """
    Converts a JSON file to a CSV file.
    """
    worker_csvs = [
        action_keyword_csv,
        action_description_parent_csv,
        action_title_application_csv
    ]
    paths = [func() for func in worker_csvs]
    print(f"Merging converted CSVs at : {paths}")
    result_path = merge_converted_csvs(paths)
    print(f"Dataset CSV created at : {result_path}")

def action_keyword_csv():
    """
    Stores a csv of action and keyword pairs.
    """
    file_path = '/app/data/conversions/action_with_keywords.csv'
    if os.path.exists(file_path):
        os.remove(file_path)
    json_path = '/app/data/default.tasks.search'
    df = pd.read_json(json_path)
    action_to_keywords_mapping = {}
    for _, row in df.iterrows():
        item = row['search_keywords']
        keyword = item['keyword']
        list_dict_actions = item['value']
        for d in list_dict_actions:
            action = d['action']
            if action not in action_to_keywords_mapping:
                action_to_keywords_mapping[action] = list()
            action_to_keywords_mapping[action].append(keyword)
    # Convert to list of dictionaries for DataFrame
    data = []
    for action, keywords in action_to_keywords_mapping.items():
        # Flatten keywords if they contain lists and convert to strings
        flattened_keywords = []
        for keyword in keywords:
            if isinstance(keyword, list):
                flattened_keywords.extend([str(k) for k in keyword])
            else:
                flattened_keywords.append(str(keyword))
        
        # Remove duplicates while preserving order
        unique_keywords = list(dict.fromkeys(flattened_keywords))
        keywords_str = ', '.join(unique_keywords)
        
        data.append({
            'action': action,
            'keywords': keywords_str
        })
    
    # Create DataFrame and write to CSV
    wdf = pd.DataFrame(data)
    wdf.to_csv(file_path, index=False)
    return file_path

def action_description_parent_csv():
    """
    Stores a csv of action and description pairs.
    """
    file_path = '/app/data/conversions/action_with_description_and_parent.csv'
    if os.path.exists(file_path):
        os.remove(file_path)
    json_path = '/app/data/descriptions.json'
    df = pd.read_json(json_path)
    action_to_description_parent_mapping = {}
    task_description = df['task_tree_descriptions']
    for row in task_description:
        action = row['action']
        description = row.get('description', None)
        parent = row.get('parent', None)
        if action not in action_to_description_parent_mapping:
            action_to_description_parent_mapping[action] = [None, None]
        if description:
            action_to_description_parent_mapping[action][1] = description
        if parent:
            action_to_description_parent_mapping[action][0] = parent
    # Convert to list of dictionaries for DataFrame
    data = []
    for action, (parent, description) in action_to_description_parent_mapping.items():
        data.append({
            'action': action,
            'parent': parent,
            'description': description
        })
    wdf = pd.DataFrame(data)
    wdf.to_csv(file_path, index=False)
    return file_path

def extract_keys_from_app(df, idx):
    """
    Extract keys from dataframe based on index.
    """
    keys = []
    browser = df['tasks_browse']
    columns = browser.iloc[0]
    data = columns[idx]
    for item in data['items']:
        keys.append(item)
    return keys

def populate_action_title_application_mapping(action_title_application_type_mapping, keys, df):
    """
    Populate action title application type mapping.
    """
    for item in keys:
        key = item.get('task', None)
        if key:
            application_type = item['name']
            data = df[key]['columns']
            for element in data:
                items = element.get('items', [])
                if len(items) == 1 and 'action' not in items[0]:
                    continue
                for action_dict in items:
                    if task := action_dict.get('task', None):
                        name = action_dict.get('name', None)
                        keys.append({'task': task, 'name': name})
                        continue
                    action = action_dict.get('action', None)
                    title = action_dict.get('name', None)
                    if action and title:
                        action_title_application_type_mapping[action] = (title, application_type)
        else:
            if action := item.get('action', None):
                print(f"Processing action: {action}")
                title = item.get('name', None)
                application_type = 'Unknown'
                action_title_application_type_mapping[action] = (title, application_type)

def action_title_application_csv():
    """
    Convert a json of action and title pairs to csv.
    """
    file_path = '/app/data/conversions/action_with_title_and_application.csv'
    if os.path.exists(file_path):
        os.remove(file_path)
    json_path = '/app/data/default.tasks.menu'
    df = pd.read_json(json_path)
    app_keys = extract_keys_from_app(df, 0)
    related_components = extract_keys_from_app(df, 1)
    task_keys = extract_keys_from_app(df, 2)
    action_title_application_type_mapping = {}
    populate_action_title_application_mapping(action_title_application_type_mapping, app_keys, df)
    populate_action_title_application_mapping(action_title_application_type_mapping, related_components, df)
    populate_action_title_application_mapping(action_title_application_type_mapping, task_keys, df)
    # Convert to list of dictionaries for DataFrame
    data = []
    for action, (title, application_type) in action_title_application_type_mapping.items():
        data.append({
            'action': action,
            'title': title,
            'application_type': application_type
        })
    wdf = pd.DataFrame(data)
    wdf.to_csv(file_path, index=False)
    return file_path

def merge_converted_csvs(paths, clean_up=True):
    """
    Merges all converted CSV files into a single CSV file.
    """
    result_path = '/app/data/conversions/dataset.csv'
    if os.path.exists(result_path):
        os.remove(result_path)
    # final csv has the columns: action, keywords, parent, description, title, application_type
    merged_df = pd.DataFrame(columns=[
        'action',
        'keywords',
        'parent',
        'description',
        'title',
        'application_type'
    ])
    for path in paths:
        df = pd.read_csv(path)
        # update the row for corresponding action with available columns
        for _, row in df.iterrows():
            action = row['action']
            if action not in merged_df['action'].values:
                merged_df = pd.concat([merged_df, pd.DataFrame([{'action': action}])], ignore_index=True)
            for col in df.columns:
                if col != 'action':
                    merged_df.loc[merged_df['action'] == action, col] = row[col]
    # sort by action
    merged_df = merged_df.sort_values(by='action').reset_index(drop=True)
    # print total number of rows
    print(f"Total number of rows in merged dataset: {len(merged_df)}")
    merged_df.to_csv(result_path, index=False)
    if clean_up:
        for path in paths:
            if os.path.exists(path):
                os.remove(path)
    return result_path



    
