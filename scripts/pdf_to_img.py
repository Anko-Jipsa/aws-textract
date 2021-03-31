import sys
import os
from pdf2image import convert_from_path


def to_jpg(input_path: str, save_path: str):
    """ Convert a PDF file pages into JPEG files.

    Args:
        file_path (str): Input directory.
        save_path (str): Save directory.
    """
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    images = convert_from_path(input_path, 500)
    file_name = input_path.split('.')[0].split('/')[-1]

    for i, page in enumerate(images):
        img = os.path.join(save_path, f'{file_name}-{i}.jpg')
        page.save(img, 'JPEG')
        print(f"IMG SAVED: {file_name}-{i}.jpg")


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
