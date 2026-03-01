# Fundamentals
import os
import platform

# FileTypes
import base64
import yaml

# Functionality
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()

from pathlib import Path
from openai import OpenAI

with open("settings.yaml", "r") as file:
        config = yaml.safe_load(file)

# FUNCTIONS
def openImage():
    folder = config.get("previousFolder")
    if not folder:
        folder = Path.home() / "Documents"
    
    if platform.system() == "Windows":
        selected = filedialog.askopenfilename(
            initialdir=folder,
            title="Select Image",
            filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.bmp;*.gif")],
        )
        if not selected:
            print("No file selected. Exiting.")
            exit(1)
        config["previousFolder"] = os.path.dirname(selected)
        with open("settings.yaml", "w") as file:            
            yaml.dump(config, file)

        return selected


if config.get("apiKey") is None:
    print("No API Key found in settings.yaml. Please add your OpenAI API key.")
    exit(1)

# OpenAI API Parsing
client = OpenAI(api_key=config.get("apiKey"))

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def loadImage(prompt):
    image_path = openImage()

    print("Encoding Image")
    base64_image = encode_image(image_path)
    print("Success!")
    
    print("Sending it over!")
    return client.responses.create(
        model="gpt-4.1",
        input=[
            {
                "role": "user",
                "content": [
                    { "type": "input_text", "text": prompt },
                    {
                        "type": "input_image",
                        "image_url": f"data:image/jpeg;base64,{base64_image}",
                    },
                ],
            }
        ],
    )


response = loadImage(input("Query about image? \n"))
print("Got Response!")
print("GPT:")
print(response.output_text)