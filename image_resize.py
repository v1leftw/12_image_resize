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
        help="Path to output image"
    )
    return parser.parse_args()


def validate_arguments(args):
    arg_error = None
    if args.scale and (args.height or args.width):
        arg_error = "Can not use both scale and height or width"
    if check_argument(args.scale):
        arg_error = "Scale can not be less or equal to zero"
    if check_argument(args.width):
        arg_error = "Width can not be less or equal to zero"
    if check_argument(args.height):
        arg_error = "Heigth can not be less or equal to zero"
    if args.scale and args.height and args.width is None:
        arg_error = "No resize arguments specified"
    return args, arg_error


def check_argument(arg):
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


def resize_image(image, width, height, scale):
    return image.resize(calucalate_proportions(
        image,
        width,
        height,
        scale
    ))


def calucalate_proportions(image, width, height, scale):
    user_image_height, user_image_width = image.size
    image_proportions = user_image_width/user_image_height
    if scale:
        height = round(user_image_height * scale)
        width = round(user_image_width * scale)
    if width is None:
        width = round(user_image_width * image_proportions)
    if height is None:
        height = round(user_image_height * image_proportions)
    return height, width


def generate_output_path(original_path, size, new_path=None):
    height, width = size
    ext = os.path.splitext(os.path.abspath(original_path))[1]
    if new_path is None:
        output_path = "{}__{}x{}{}".format(
            original_path.split(".")[0],
            width,
            height,
            ext
        )
    else:
        filename = os.path.basename(original_path)
        output_path = "{}{}__{}x{}{}".format(
            new_path.split(".")[0],
            filename.split(".")[0],
            width,
            height,
            ext
        )
    return output_path


def get_path(output_path):
    if output_path is None:
        _path_to_file = generate_output_path(
            arguments.path,
            modified_image.size
        )
    elif is_file(output_path):
        _path_to_file = arguments.output
    else:
        _path_to_file = generate_output_path(
            arguments.path,
            modified_image.size,
            arguments.output
        )
    return _path_to_file


def is_file(path):
    return bool(os.path.splitext(path)[1])


def save_image(image, path):
    try:
        image.save(path)
        return True
    except IOError:
        return False


def is_proportions_error(original_image, resized_image):
    _height, _width = original_image.size
    height, width = resized_image.size
    return round(_width/_height, 2) != round(width/height, 2)


if __name__ == "__main__":
    arguments, error = validate_arguments(get_args())
    if error:
        exit(error)
    user_image = open_image(arguments.path)
    if user_image is None:
        exit("Can not open image")
    image_height, image_width = user_image.size
    modified_image = resize_image(
        user_image,
        arguments.width,
        arguments.height,
        arguments.scale
    )
    if is_proportions_error(user_image, modified_image):
        print("Proportions of given image and output image are not equal")
    path_to_file = get_path(arguments.output)
    if save_image(modified_image, path_to_file):
        print("Image saved. Path to file: {}".format(path_to_file))
    else:
        print("Could not save image")
    user_image.close()
