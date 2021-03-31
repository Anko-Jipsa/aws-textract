import sys
import os
from pdf2image import convert_from_path


def to_jpg(file_path, save_path):
    images = convert_from_path(file_path, 500)

    if not os.path.exists(save_path):
        os.makedirs(save_path)

    for i, page in enumerate(images):
        _file = os.path.join(save_path, f'page-{i}.jpg')
        page.save(_file, 'JPEG')
        print(f"IMG SAVED: page {i}.jpg")


if __name__ == "__main__":
    # cml inputs.
    input_path = sys.argv[1]
    save_path = sys.argv[2]

    if not os.path.exists(input_path):
        raise ValueError(
            f"Directory: '{input_path}' does not exist, check the path again.")

    print("***** Converting PDF to JPG *****")
    print("--------------------------------")
    print(f"INPUT PDF FILE: {input_path} \n")
    print(f"IMG SAVE LOCATION: {save_path}")
    print("-------------------------------- \n")
    to_jpg(input_path, save_path)
