import gradio as gr
import numpy as np 
from PIL import Image
from transformers import AutoProcessor, BlipForConditionalGeneration

processor = AutoProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")


def caption_image(input_image : np.ndarray):
    # Convert numpy array to PIL Image and Convert to RGB
    raw_image = Image.fromarray(input_image).convert("RGB")

    # Process the image 
    # image = Image.open(img_path).convert('RGB')
    text = "The image is about "
    input = processor(images=raw_image, text=text, return_tensors='pt')

    # Generate a caption for the image 
    outputs = model.generate(**input, max_length=100)

    # Decode the generated tokens to text
    caption = processor.decode(outputs[0], skip_special_tokens=True)

    return caption

iface = gr.Interface(
    fn=caption_image,
    inputs = gr.Image(),
    outputs = 'text',
    title="Image Captioning",
    description = "Gradio web app for generating image captions "
)

iface.launch()
