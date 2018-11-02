from PIL import Image
import argparse
import re


class CheckPossibilityToScale(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        print(namespace)
        if namespace.height is not None or namespace.width is not None:
            parser.error("Can not scale image, cause width "
                         "or height has been set")
        else:
            # In order if user specifies params after scale call
            print("Scale has been set. Width and height will be ignored")
            namespace.scale = values


def get_args():
    parser = argparse.ArgumentParser(description="Enter the path:")
    parser.add_argument("-path", required=True, help="Path to file")
    parser.add_argument("-height", help="Height of output image")
    parser.add_argument("-width", help="Width of output image")
    parser.add_argument(
        "-scale",
        help="Scale of output image",
        action=CheckPossibilityToScale
    )
    parser.add_argument("-output", help="Path that stores output image")
    return parser.parse_args()


def validate_arguments(args):
    try:
        int(args.scale)
        int(args.width)
        int(args.height)
    except ValueError:
        return None


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
        return image.resize((height, user_image_width * image_proportions))
    if height is None:
        return image.resize((user_image_height * image_proportions, width))
    return image.resize((height, width))


def rescale_image(image, scale):
    height, width = image.size
    scale = int(scale)
    return image.resize((height * scale, width * scale))


def generate_output_path(path, size):
    height, width = size
    return re.sub(r"\.", "__{}x{}.".format(height, width), path)


if __name__ == "__main__":
    arguments = get_args()
    if validate_arguments(arguments) is None:
        exit("Argument was specified in wrong format")
    user_image = open_image(arguments.path)
    image_height, image_width = user_image.size
    if user_image is None:
        exit("Can not open image")
    if arguments.scale is not None:
        modified_image = rescale_image(user_image, arguments.scale)
    else:
        if arguments.width / arguments.height != image_width / image_height:
            print("Proportions of given image and output image are not equal")
        modified_image = resize_image(
            user_image,
            arguments.width,
            arguments.height
        )
    if arguments.output is None:
        output_path = generate_output_path(arguments.path, modified_image.size)
    else:
        output_path = generate_output_path(
            arguments.output,
            modified_image.size
        )
    try:
        modified_image.save(output_path)
        print("Image saved. Path to file: {}".format(output_path))
    except IOError:
        exit("Could not save image")
