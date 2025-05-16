import requests
import os

def download_pdf(url, save_path):
    try:
        response = requests.get(url)
        response.raise_for_status()  # raise error for bad responses
        with open(save_path, 'wb') as f:
            f.write(response.content)
        print(f"✅ PDF successfully downloaded to: {save_path}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to download PDF: {e}")

if __name__ == "__main__":
    url = input("Enter the URL of the PDF to download: ").strip()

    # Automatically generate filename from URL
    filename = os.path.basename(url)
    save_path = os.path.join(".", filename)

    download_pdf(url, save_path)

