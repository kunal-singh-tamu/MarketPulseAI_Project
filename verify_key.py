import os
from dotenv import load_dotenv
import google.generativeai as genai

# 1. Force load the .env file
print("--- LOADING .ENV FILE ---")
loaded = load_dotenv() 
print(f"Did .env load? {loaded}")

# 2. Try to get the key
api_key = os.environ.get("GOOGLE_API_KEY")

if not api_key:
    print("❌ ERROR: Key is None. Check your .env file name and format.")
    print("Make sure the file is named exactly '.env' (no .txt)")
    print("Make sure the line inside reads: GOOGLE_API_KEY=AIzaSy...")
else:
    print(f"✅ Key Found: {api_key[:5]}... (hidden)")
    
    # 3. Test the Key with a real request
    print("\n--- TESTING GOOGLE CONNECTION ---")
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content("Say 'Hello' if this works.")
        print(f"✅ SUCCESS! Google responded: {response.text.strip()}")
    except Exception as e:
        print(f"❌ AUTH ERROR: The key was found, but rejected by Google.")
        print(f"Error details: {e}")