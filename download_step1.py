import urllib.request
import os

# The identified high-quality technical image for Step 1
url = "https://s.alicdn.com/@sc04/kf/Hd8cb815bb7f742a689f725a070914e82Y.jpg_300x300.jpg"
desktop_path = "step1_screws.jpg"

try:
    print(f"Downloading technical frame to: {desktop_path}")
    urllib.request.urlretrieve(url, desktop_path)
    print("Success: Technical frame saved to Desktop.")
except Exception as e:
    print(f"Failed to download image: {str(e)}")
