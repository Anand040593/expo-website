from PIL import Image
import os

img_path = r"c:\Users\anand\Downloads\Expo_website\extracted_images\image_p0_0.png"
output_dir = r"c:\Users\anand\Downloads\Expo_website\assets"
os.makedirs(output_dir, exist_ok=True)

img = Image.open(img_path)
width, height = img.size

# The logo is in the top right corner. The image seems split horizontally in half for content vs logo/dates.
# So x starts around width/2. y starts from top. Let's estimate:
# x from width/2 to width, y from 0 to height/3.
left = width * 0.52
top = 0
right = width
bottom = height * 0.35

logo = img.crop((left, top, right, bottom))
logo.save(os.path.join(output_dir, "logo.png"))
print("Logo cropped and saved successfully.")
