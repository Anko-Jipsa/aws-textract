#%%
import run_api

PDF_FILE = "example_input/TSB_2020Q4.pdf"
IMG_PATH = "example_output/TSB/img"
CSV_SAVE_PATH = "example_output/TSB/csv"
S3BUCKET = "textract-bucket-ver1"
BUCKET_DIR = "TSB"

run_api.main(PDF_FILE, IMG_PATH, CSV_SAVE_PATH, S3BUCKET, BUCKET_DIR)

# %%
