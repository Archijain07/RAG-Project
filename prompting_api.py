import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load .env
load_dotenv()
GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini API
genai.configure(api_key=GOOGLE_API_KEY)

def main():
    print("🔍 Ask anything to Gemini!")
    prompt = input("📝 Enter your prompt: ")

    try:
        # Load Gemini model
        model = genai.GenerativeModel("gemini-2.0-flash")
        
        # Generate response
        response = model.generate_content(prompt)

        # Display response
        print("\n🤖 Response:")
        print(response.text.strip())

    except Exception as e:
        print("❌ Error:", e)

if __name__ == "__main__":
    main()

