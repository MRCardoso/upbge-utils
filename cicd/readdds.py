from PIL import Image
import sys

if len(sys.argv) < 1:
    print("define file path")
    exit()

def read_dds(file_path):
    try:
        with Image.open(file_path) as img:
            # Ensure the image is in a format compatible with Pillow
            img.load()
            return img
    except IOError:
        print("Unable to open DDS file:", file_path)
        return None

# Example usage:
dds_file_path = sys.argv[1]
print(dds_file_path)
dds_image = read_dds(dds_file_path)

if dds_image:
    print("Successfully loaded DDS file:", dds_file_path)
    dds_image.show()  # Display the image using the default image viewer
