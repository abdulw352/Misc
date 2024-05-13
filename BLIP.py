import requests
from PIL import Image
from transformers import AutoProcessor, BlipForConditionalGeneration

# Load the pretrained processor and model
processor = AutoProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# image
img_path = "cat.jpg"

# Convert the image to RGB format 
image = Image.open(img_path).convert('RGB')

text = "the image is about "
input = processor(images=image, text=text, return_tensors='pt')

# Generate a caption 
outputs = model.generate(**input, max_length=50)

# Decode the generated tokens to text
caption = processor.decode(outputs[0], skip_special_tokens=True)
# print the caption
print(caption)

