"""
#TODO:
- Improve Docstring.

"""
import webbrowser, os
import json
import boto3
import io
from io import BytesIO
import sys
from pprint import pprint
import pandas as pd


def get_rows_columns_map(table_result: object, blocks_map):
    """ Get rows from Textract API generated block object.

    Args:
        table_result (object): Text object generated from Textract API.
        blocks_map ([type]): TBD.

    Returns:
        [type]: [description]
    """
    rows = {}
    for relationship in table_result['Relationships']:
        if relationship['Type'] == 'CHILD':
            for child_id in relationship['Ids']:
                cell = blocks_map[child_id]
                if cell['BlockType'] == 'CELL':
                    row_index = cell['RowIndex']
                    col_index = cell['ColumnIndex']
                    if row_index not in rows:
                        # create new row
                        rows[row_index] = {}

                    # get the text value
                    rows[row_index][col_index] = get_text(cell, blocks_map)
    return rows


def get_text(result, blocks_map):
    text = ''
    if 'Relationships' in result:
        for relationship in result['Relationships']:
            if relationship['Type'] == 'CHILD':
                for child_id in relationship['Ids']:
                    word = blocks_map[child_id]
                    if word['BlockType'] == 'WORD':
                        text += word['Text'] + ' '
                    if word['BlockType'] == 'SELECTION_ELEMENT':
                        if word['SelectionStatus'] == 'SELECTED':
                            text += 'X '
    return text


def get_table_results(s3bucket: str, document_name: str) -> dict:
    """ Generate CSV data from image files stored in S3 bucket using Textract.

    Args:
        s3bucket (str): S3 bucket name.
        document_name (str): Name of the image file in S3 bucket.

    Returns:
        dict: Dictionary contains multiple pd.DataFrames.
    """
    # Textract API
    client = boto3.client('textract')
    response = client.analyze_document(
        Document={'S3Object': {
            "Bucket": s3bucket,
            "Name": document_name
        }},
        FeatureTypes=['TABLES'])

    # Get the text blocks
    blocks = response['Blocks']

    blocks_map = {}
    table_blocks = []
    for block in blocks:
        blocks_map[block['Id']] = block
        if block['BlockType'] == "TABLE":
            table_blocks.append(block)

    if len(table_blocks) <= 0:
        print("No table found")

    table_dict = {}
    for index, table in enumerate(table_blocks):
        table_dict[index] = generate_table(table, blocks_map, index + 1)

    return table_dict


def generate_table(table_result, blocks_map, table_index):
    rows = get_rows_columns_map(table_result, blocks_map)

    return pd.DataFrame(rows).T


def export_csv(s3bucket: str, document_obj: str, save_path: str,
               output_name: str):
    """ Export CSV files.

    Args:
        s3bucket (str): S3 bucket name.
        document_obj (str): TBD.
        save_path (str): CSV save directory.
        output_name (str): CSV output file name.
    """
    table_dict = get_table_results(s3bucket, document_obj)
    file_id = document_obj.split('.')[0][-1]

    if not os.path.exists(save_path):
        os.makedirs(save_path)

    for index, table in table_dict.items():
        _save_path = os.path.join(save_path,
                                  f"{output_name}-{file_id}_{index}.csv")
        table.to_csv(_save_path)


def textract_api(s3bucket: str, bucket_path: str, save_path: str):
    """ Run Textract API via connected S3 bucket object.

    Args:
        s3bucket (str): S3 bucket name.
        bucket_path (str): Directory within the bucket.
        save_path (str): CSV save directory.
    """
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(s3bucket)
    for bucket_obj in bucket.objects.filter(Prefix=bucket_path):
        document_obj = bucket_obj.key
        print(f"EXPORTING: {document_obj}")
        export_csv(s3bucket, document_obj, save_path, bucket_path)


if __name__ == "__main__":
    csv_save_path = sys.argv[2]  # csv save location
    s3bucket = sys.argv[3]  # s3 bucket name
    bucket_dir = sys.argv[4]  # separate directory within s3 bucket

    print("******* Running Textract *******")
    print("--------------------------------")
    print(f"S3 Bucket: {s3bucket} \n")
    print(f"S3 Directory: {bucket_dir} \n")
    print(f"CSV SAVE PATH: {csv_save_path}")
    print("-------------------------------- \n")
    textract_api(s3bucket, bucket_dir, csv_save_path)
