import urllib.request
import os

files = {
    "step4_pick.jpg": "https://guide-images.cdn.ifixit.com/igi/1rXfWqQY4caQAybt.large",
    "step5_battery.jpg": "https://guide-images.cdn.ifixit.com/igi/LxlBZKHLNudrtKj4.large",
    "step6_seal.jpg": "https://guide-images.cdn.ifixit.com/igi/4sSlc4n44yLqiOqB.large"
}

output_dir = "downloads"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

for name, url in files.items():
    path = os.path.join(output_dir, name)
    try:
        print(f"Downloading {url} to {path}...")
        urllib.request.urlretrieve(url, path)
        print(f"Success: {name}")
    except Exception as e:
        print(f"Failed to download {name}: {str(e)}")
