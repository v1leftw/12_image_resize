from PIL import Image
import argparse
import os


def validate_path(path):
    if os.path.exists(path):
        return path
    else:
        raise argparse.ArgumentTypeError("Path does not exists")


def get_args():
    parser = argparse.ArgumentParser(description="Enter the path:")
    parser.add_argument(
        "-path",
        required=True,
        help="Path to file",
        type=validate_path
    )
    parser.add_argument(
        "-height",
        help="Height of output image",
        default=None,
        type=int
    )
    parser.add_argument(
        "-width",
        help="Width of output image",
        default=None,
        type=int
    )
    parser.add_argument(
        "-scale",
        help="Scale of output image",
        default=None,
        type=float
    )
    parser.add_argument(
        "-output",
        help="Directory that stores output image",
        type=validate_path
    )
    args = parser.parse_args()
    if args is None:
        parser.error("No arguments specified")
    if args.scale and (args.height or args.width):
        parser.error("Can not use both scale and height or width")
    if checker(args.scale) or checker(args.width) or checker(args.height):
        parser.error("Arguments can not be less or equal to zero")
    if args.scale and args.height and args.width is None:
        parser.error("No resize arguments specified")
    return args


def checker(arg):
    if arg is None:
        return False
    if arg > 0:
        return False
    return True


def open_image(path_to_image):
    try:
        image = Image.open(path_to_image)
        return image
    except OSError:
        return None


def resize_image(image, width, height):
    user_image_height, user_image_width = image.size
    image_proportions = user_image_width/user_image_height
    if width is None:
        return image.resize((
            height,
            round(user_image_width * image_proportions)
        ))
    if height is None:
        return image.resize((
            round(user_image_height * image_proportions),
            width
        ))
    return image.resize((height, width))


def rescale_image(image, scale):
    height, width = image.size
    return image.resize((round(height * scale), round(width * scale)))


def generate_output_path(original_path, size, new_path=None):
    height, width = size
    ext = os.path.splitext(os.path.abspath(original_path))
    if new_path is None:
        return "{}__{}x{}{}".format(
            original_path.split(".")[0],
            width,
            height,
            ext[1]
        )
    filename = os.path.basename(original_path)
    return "{}{}__{}x{}{}".format(
        new_path.split(".")[0],
        filename.split(".")[0],
        width,
        height,
        ext[1]
    )


def save_image(image, path):
    try:
        image.save(path)
        return True
    except IOError:
        return False


def get_proportions_error(original_image, resized_image):
    _height, _width = original_image.size
    height, width = resized_image.size
    if round(_width/_height, 2) != round(width/height, 2):
        return "Proportions of given image and output image are not equal"
    return None


if __name__ == "__main__":
    arguments = get_args()
    user_image = open_image(arguments.path)
    if user_image is None:
        exit("Can not open image")
    image_height, image_width = user_image.size
    if arguments.scale is not None:
        modified_image = rescale_image(user_image, arguments.scale)
    else:
        modified_image = resize_image(
            user_image,
            arguments.width,
            arguments.height
        )
        print(get_proportions_error(
            user_image,
            modified_image
        ))
    if arguments.output is None:
        output_path = generate_output_path(arguments.path, modified_image.size)
    else:
        output_path = generate_output_path(
            arguments.path,
            modified_image.size,
            arguments.output
        )
    if save_image(modified_image, output_path):
        print("Image saved. Path to file: {}".format(output_path))
    else:
        print("Could not save image")
    user_image.close()
