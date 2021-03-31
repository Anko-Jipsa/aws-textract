# aws-textract
AWS Textract

Repo includes:
- run_api.py # execute the Textract API with images stored in the S3 bucket
- upload_files.py # upload local images to S3 bucket
- pdf_to_img.py # convert pdf file into images (JPEG) and store into the local folder

Example:

Running the Textract API (Dataset is stored in S3 bucket)
```console
jk@mbp:~$ python run_api.py example_input/TSB_2020Q4.pdf example_output/TSB/img example_output/TSB/csv textract-bucket-ver1 TSB
```

```python
import run_api

PDF_FILE = "example_input/TSB_2020Q4.pdf"
IMG_PATH = "example_output/TSB/img"
CSV_SAVE_PATH = "example_output/TSB/csv"
S3BUCKET = "textract-bucket-ver1"
BUCKET_DIR = "TSB"

run_api.main(PDF_FILE, IMG_PATH, CSV_SAVE_PATH, S3BUCKET, BUCKET_DIR)
```

















