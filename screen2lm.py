from PIL import ImageGrab
import pytesseract
import requests
import time
import pyautogui

LM_STUDIO_URL = "http://localhost:1234/v1/chat/completions"
HEADERS = {"Content-Type": "application/json"}

# Tesseract path
pytesseract.pytesseract.tesseract_cmd = r"Path\To\Tesseract-OCR\tesseract.exe"

def get_screen_center_bbox(width=700, height=200): # Change the bbox size
    screen_w, screen_h = pyautogui.size()
    left = (screen_w - width) // 2
    top = (screen_h - height) // 2
    right = left + width
    bottom = top + height
    return (left, top, right, bottom)

def get_text_from_screen(bbox):
    img = ImageGrab.grab(bbox)
    text = pytesseract.image_to_string(img)
    return text.strip()

def ask_lm_studio(prompt_text):
    data = {
        "model": "gemma-3-12b-it",  # LM Studio model name
        "messages": [
            {"role": "user", "content": prompt_text}
        ],
        "temperature": 0.7
    }
    response = requests.post(LM_STUDIO_URL, headers=HEADERS, json=data)
    return response.json()["choices"][0]["message"]["content"]

while True:
    bbox = get_screen_center_bbox()
    text = get_text_from_screen(bbox)
    if text:
        print("🧾 Perceived text:", text)
        reply = ask_lm_studio("Answer this:\n" + text)
        print("🤖 AI:", reply)
    time.sleep(2) # Delay for each process
