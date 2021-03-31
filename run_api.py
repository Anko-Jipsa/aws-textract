import os
import sys
from scripts import *


def main(pdf_file, img_save_path, csv_save_path, s3bucket, bucket_path):
    if not os.path.exists(pdf_file):
        raise ValueError(
            f"Directory: '{pdf_file}' does not exist, check the path again.")

    print("++++++++++ Running Textract API +++++++++")
    print("--------------------------------")
    print(f"PDF FILE: {pdf_file} \n")
    print(f"IMG SAVE LOCATION: {img_save_path}")
    print("-------------------------------- \n")
    to_jpg(input_path=pdf_file, save_path=img_save_path)
    print("******* Converted PDF to images ******* \n \n")

    print("--------------------------------")
    print(f"Image Folder Path: {img_save_path}")
    print(f"S3 Bucket: {s3bucket}")
    print(f"S3 Directory: {bucket_path}")
    print("-------------------------------- \n")
    upload_files(input_path=img_save_path,
                 s3bucket=s3bucket,
                 bucket_path=bucket_path)
    print("******* Uploaded images to S3 ******* \n \n")

    print("--------------------------------")
    print(f"S3 Bucket: {s3bucket} \n")
    print(f"S3 Directory: {bucket_path} \n")
    print(f"SAVE PATH: {csv_save_path}")
    print("-------------------------------- \n")
    textract_api(s3bucket, bucket_path, csv_save_path)
    print("************ Saved csv files ************ \n \n")
    print("++++++++++ Completed +++++++++")


if __name__ == "__main__":
    # cml inputs.
    pdf_file = sys.argv[1]  # input pdf file
    img_save_path = sys.argv[2]  # img save path
    csv_save_path = sys.argv[3]  # csv save path
    s3bucket = sys.argv[4]  # s3 bucket name
    bucket_path = sys.argv[5]  # separate directory within s3 bucket

    main(pdf_file, img_save_path, csv_save_path, s3bucket, bucket_path)