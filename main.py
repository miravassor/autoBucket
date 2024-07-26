import os
import argparse
from PIL import Image


def process_folder(folder_path, canvas_size, output_folder):
    if not os.path.exists(output_folder):
        try:
            os.makedirs(output_folder)
        except OSError:
            print("Creation of the directory %s failed, check rights" % output_folder)
            exit(1)

    for filename in os.listdir(folder_path):
        if filename.endswith((".png", ".jpg", ".jpeg")):
            img_path = os.path.join(folder_path, filename)
            output_path = os.path.join(output_folder, filename)
            procede(img_path, canvas_size, output_path)


def procede(img_path, canvas_size, output_path):
    try:
        img = Image.open(img_path)
    except IOError:
        print("Can't open (check rights)", img_path)
        exit(1)

    canvas = Image.new(img.mode, canvas_size, (255, 255, 255))

    img_width, img_height = img.size
    canvas_width, canvas_height = canvas_size

    img_ratio = img_width / img_height
    canvas_ratio = canvas_width / canvas_height

    if img_ratio > canvas_ratio:
        new_width = canvas_width
        new_height = int(new_width / img_ratio)
    else:
        new_height = canvas_height
        new_width = int(new_height * img_ratio)

    resized_img = img.resize((new_width, new_height))

    offset = ((canvas_width - new_width) // 2, (canvas_height - new_height) // 2)
    canvas.paste(resized_img, offset)
    canvas.save(output_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Auto image padding")
    parser.add_argument("folder_path", help="Path to the folder containing the images")
    parser.add_argument("-o", "--output_folder", help="Path to the output folder (default: 'output' subfolder within "
                                                      "the input folder)", default="")
    parser.add_argument("-s", "--size", type=int, nargs=2, default=(1024, 1024),
                        metavar=("width", "height"), help="Final dimensions (width, height)")

    args = parser.parse_args()

    folder_path = args.folder_path
    if not args.output_folder:
        output_folder = os.path.join(folder_path, "output")
    else:
        output_folder = args.output_folder

    folder_path = args.folder_path
    canvas_size = tuple(args.size)

    if not os.path.exists(folder_path):
        print(f"Error: Input folder '{folder_path}' does not exist.")
        exit(1)

    try:
        os.makedirs(output_folder, exist_ok=True)
    except OSError as e:
        print(f"Error creating output folder: {e}")

    process_folder(folder_path, canvas_size, output_folder)
