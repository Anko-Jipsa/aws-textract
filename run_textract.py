import webbrowser, os
import json
import boto3
import io
from io import BytesIO
import sys
from pprint import pprint
import pandas as pd


def get_rows_columns_map(table_result, blocks_map):
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


def get_table_results(file_path):

    with open(file_path, 'rb') as file:
        img_test = file.read()
        bytes_test = bytearray(img_test)
        print('Image loaded', file_path)

    # process using image bytes
    # get the results
    client = boto3.client('textract')

    response = client.analyze_document(Document={'Bytes': bytes_test},
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
        return "<b> NO Table FOUND </b>"

    table_dict = {}
    for index, table in enumerate(table_blocks):
        table_dict[index] = generate_table(table, blocks_map, index + 1)

    return table_dict


def generate_table(table_result, blocks_map, table_index):
    rows = get_rows_columns_map(table_result, blocks_map)

    # create Pandas DataFrame object
    table = pd.DataFrame(rows).T
    return table


def export_csv(file_path, save_path, output_name):
    table_dict = get_table_results(file_path)
    file_id = file_path.split('.')[0][-1]

    for index, table in table_dict.items():
        _save_path = os.path.join(save_path,
                                  f"{output_name}-{file_id}_{index}.csv")
        table.to_csv(_save_path)


def main(s3bucket, bucket_path, save_path):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(s3bucket)
    for bucket_obj in bucket.objects.filter(Prefix=bucket_path):
        file_obj = bucket_obj.key
        export_csv(file_obj, save_path, bucket_path)


if __name__ == "__main__":

    s3bucket = sys.argv[1]
    bucket_path = sys.argv[2]
    save_path = sys.argv[3]
    if not os.path.exists(save_path):
        raise ValueError(
            f"SAVE DIR: '{save_path}' does not exist, check the path again.")
    print("--------------------------------")
    print(f"S3 Bucket: {s3bucket} \n")
    print(f"S3 Object Dir: {bucket_path} \n")
    print(f"SAVE DIR: {save_path}")
    print("-------------------------------- \n")
    main(s3bucket, save_path, bucket_path)
