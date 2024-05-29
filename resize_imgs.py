from PIL import Image


def resize_image(image_path, output_path):
    """
    Resizes an image to half its original height and width.

    Args:
        image_path: Path to the input image file.
        output_path: Path to save the resized image file.
    """
    try:
        # Open the image
        image = Image.open(image_path)

        # Get the original size
        width, height = image.size

        # Calculate new dimensions (half the size)
        new_width = round(width * 0.5)
        new_height = round(height * 0.5)

        # Resize the image
        resized_image = image.resize((new_width, new_height))

        # Save the resized image
        resized_image.save(output_path)
        print(f"Image resized and saved to: {output_path}")
    except OSError as e:
        print(f"Error: Could not open image file: {e}")


if __name__ == '__main__':
    image_path = "imgs/" + input("Enter image path: ") + ".jpg"
    output_path = f"{image_path}"

    resize_image(image_path, output_path)
