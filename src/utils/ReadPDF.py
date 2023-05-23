import cv2
import pytesseract
import os
import numpy as np
from PIL import Image, ImageEnhance


def cv2_preprocess(image_path):
    img = cv2.imread(image_path)

    # convert to black and white if not already
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # remove noise
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    img = cv2.erode(img, kernel, iterations=1)

    # apply a blur
    # gaussian noise
    img = cv2.threshold(
        cv2.GaussianBlur(img, (9, 9), 0), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )[1]

    cv2.imwrite("new.jpg", img)
    return "new.jpg"


def pil_enhance(image_path):
    image = Image.open(image_path)
    contrast = ImageEnhance.Contrast(image)
    contrast.enhance(2).save("new2.jpg")
    return "new2.jpg"


# Directory containing the images
image_dir = os.path.dirname(__file__) + "/../images/"

# Output file
output_file = "output.txt"

# Open the output file
with open(output_file, "w") as f:
    # Loop over all files in the image directory
    for i in range(1, 2):  # assuming you have less than 1000 pages
        filename = (
            f"The-Quran-A-Complete-Revelation-Ed-3-notes_Page_{str(i).zfill(3)}.png"
        )
        image_path = os.path.join(image_dir, filename)

        if os.path.isfile(image_path):
            print(f"Processing {filename}...")

            # Preprocess and enhance the image
            img = cv2.imread(pil_enhance(cv2_preprocess(image_path)))

            # Extract text from the image
            text = pytesseract.image_to_string(img)

            # Write the extracted text to the output file
            f.write(text + "\n")

            print(f"Finished processing {filename}.")

print("Text extraction complete.")
