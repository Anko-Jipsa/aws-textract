# aws-textract
AWS Textract

Repo includes:
- run_textract.py # runs the Textract API with images stored in the S3 bucket
- upload_files.py # upload local images to S3 bucket
- pdf_to_img.py # convert pdf file into images (JPEG) and store into the local folder

Example:

Running the Textract API (Dataset is stored in S3 bucket)
```console
jk@mbp:~$ python run_textract.py bucket-nanme /output_save_loc bucket-directory
```


Uploading the JPEG files to S3 bucket
```console
jk@mbp:~$ python upload_files.py /img_stored_loc bucket-nanme bucket-directory
```


Convert PDF files to Image file and save to JPEG files
```console
jk@mbp:~$ python pdf_to_img.py pdf_file.pdf /output_save_loc
```



















