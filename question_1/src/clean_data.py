import csv
from docx import Document
import os
import pandas as pd

def read_table_from_docx(docx_file_path):
    """
    Extracts only table from DOCX file and returns its data
    """
    document = Document(docx_file_path)
    table = document.tables[0]
    table_data = []
    for row in table.rows:
            row_data = [cell.text.replace('\xa0', '').rstrip() for cell in row.cells]
            table_data.append(row_data)
    return table_data

def save_table_to_csv(table_data, csv_file_path):
    """
    Saves table data to a CSV file.
    """
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(table_data)

docx_file_path = '..\data_raw\Assignment 1.docx'
csv_file_path = '..\data_raw\data_raw.csv'

# Check if CSV file already exists
if (not os.path.isfile(csv_file_path)):
    # Extract table from DOCX file and save to CSV
    table = read_table_from_docx(docx_file_path)
    save_table_to_csv(table, csv_file_path)

data = pd.read_csv(csv_file_path)

data['Frailty'] = data['Frailty'].apply(lambda x: 0 if x == 'N' else 1 if x == 'Y' else x)

data.dropna(inplace=True)

# or this
# data_replaced_na = data_encoded.fillna(data_encoded.mean())

data.to_csv('../data_clean/data_clean.csv', index=False)