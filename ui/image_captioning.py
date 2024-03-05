import base64
import io
import gradio as gr
import requests
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration

def get_completion(input):
    # See https://huggingface.co/Salesforce/blip-image-captioning-base#in-full-precision
    try:
        processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
        #.to("cuda")

        img_url = 'https://storage.googleapis.com/sfr-vision-language-research/BLIP/demo.jpg' 
        raw_image = input #Image.open(requests.get(img_url, stream=True).raw).convert('RGB')
        # unconditional image captioning
        inputs = processor(raw_image, return_tensors="pt")
        #.to("cuda")

        out = model.generate(**inputs)
        result = processor.decode(out[0], skip_special_tokens=True)
        return result
        
    except Exception as e:
        return str(e)

def image_to_base64_str(pil_image):
    byte_arr = io.BytesIO()
    pil_image.save(byte_arr, format='PNG')
    byte_arr = byte_arr.getvalue()
    return str(base64.b64encode(byte_arr).decode('utf-8'))

def captioner(image):
    base64_image = image_to_base64_str(image)
    result = get_completion(base64_image)
    return result[0]['generated_text']

def create_image_captioning_tab():
    gr.close_all()
    tab = gr.Interface(fn=get_completion, 
                    inputs=[gr.Image(label="Upload image", type="pil")],
                    outputs=[gr.Textbox(label="Caption")],
                    title="Image Captioning with BLIP",
                    description="Caption any image using the BLIP model",
                    allow_flagging="never",
                    #examples=["christmas_dog.jpeg", "bird_flight.jpeg", "cow.jpeg"]
                    )

    return tab