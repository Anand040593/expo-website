import fitz
import os

pdf_path = "merge.pdf"
output_dir = "extracted_images"
os.makedirs(output_dir, exist_ok=True)

doc = fitz.open(pdf_path)
print(f"Total pages: {len(doc)}")

img_count = 0
for page_index in range(len(doc)):
    page = doc[page_index]
    image_list = page.get_images()
    
    if image_list:
        print(f"Found {len(image_list)} images on page {page_index}")
    else:
        print(f"No images found on page {page_index}")
        
    for image_index, img in enumerate(page.get_images(full=True)):
        xref = img[0]
        base_image = doc.extract_image(xref)
        image_bytes = base_image["image"]
        image_ext = base_image["ext"]
        image_filename = f"image_p{page_index}_{image_index}.{image_ext}"
        image_filepath = os.path.join(output_dir, image_filename)
        with open(image_filepath, "wb") as f:
            f.write(image_bytes)
        print(f"Saved {image_filepath}")
        img_count += 1

print(f"Extracted {img_count} images.")
