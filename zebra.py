import os
import google.generativeai as genai
import requests
from PIL import Image
from io import BytesIO

def load_gemini_api_key():
    """
    Load the Gemini API key from the config.py file.
    """
    try:
        with open('config.py', 'r') as config_file:
            for line in config_file:
                if line.startswith('GEMINI_API_KEY='):
                    _, key = line.split('=', 1)
                    return key.strip('"')
    except FileNotFoundError:
        print("Error: config.py file not found.")
    except Exception as e:
        print(f"Error: {e}")
    return None

def download_image(url):
    """
    Download an image from a URL and return a PIL Image object.
    """
    headers = {
        "User-Agent": "ZebraCounter/1.0 (https://github.com/chow6482/Gemini-Zebra-Counter; chow6482@kettering.edu)"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        print(f"Image downloaded successfully: {response.status_code}")
        return Image.open(BytesIO(response.content))
    except Exception as e:
        print(f"Error downloading image: {e}")
        return None

def analyze_zebra_image(image):
    """
    Use Gemini to analyze the number of zebras in the image.
    """
    try:
        # Configure the API with the loaded Gemini API key
        genai.configure(api_key=load_gemini_api_key())

        # Use the latest Gemini model
        model = genai.GenerativeModel('gemini-1.5-flash')

        # Prompt to count zebras
        prompt = """
        Please carefully count the number of zebras in this image.
        Provide:
        1. An estimated total number of zebras
        2. A brief description of how you arrived at this estimate
        3. Any challenges in precisely counting the zebras
        """

        # Generate content with the image and prompt
        response = model.generate_content([prompt, image])
        
        return response.text

    except Exception as e:
        print(f"Error analyzing image: {e}")
        return None

# Load the Gemini API key
gemini_api_key = load_gemini_api_key()

if gemini_api_key:
    # Configure the Generative AI library with the Gemini API key
    genai.configure(api_key=gemini_api_key)
    
    # Create the Gemini model
    model = genai.GenerativeModel('gemini-pro')

    # Download and analyze the zebra image
    image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e3/Plains_Zebra_Equus_quagga.jpg/800px-Plains_Zebra_Equus_quagga.jpg"
    zebra_image = download_image(image_url)
    
    if zebra_image:
        print("\nZebra Image Analysis:")
        analysis = analyze_zebra_image(zebra_image)
        if analysis:
            print(analysis)
        else:
            print("Failed to analyze the image.")
    else:
        print("Failed to download the image.")
else:
    print("Failed to load the Gemini API key.")