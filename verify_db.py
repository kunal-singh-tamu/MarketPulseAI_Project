import os
from dotenv import load_dotenv
from supabase import create_client

def verify():
    print("--- Verifying Supabase Connection ---")
    
    # 1. Load .env
    loaded = load_dotenv()
    print(f"1. .env loaded: {loaded}")
    
    # 2. Check Keys
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    
    if not url:
        print("❌ Error: SUPABASE_URL is missing.")
    else:
        print(f"✅ SUPABASE_URL found: {url[:10]}...")
        
    if not key:
        print("❌ Error: SUPABASE_KEY is missing.")
    else:
        print(f"✅ SUPABASE_KEY found: {key[:10]}...")
        
    if not url or not key:
        print("Cannot proceed with connection test.")
        return

    # 3. Test Connection
    try:
        print("3. Attempting to connect...")
        client = create_client(url, key)
        
        # 4. Test Query
        print("4. Testing query (fetch portfolio)...")
        response = client.table("portfolio").select("count", count="exact").execute()
        print(f"✅ Connection Successful! Found {response.count} rows in 'portfolio' table.")
        
    except Exception as e:
        print(f"❌ Connection Failed: {e}")
        print("\nPossible fixes:")
        print("- Check if your SUPABASE_URL and KEY are correct.")
        print("- Ensure your IP is not blocked if you have database restrictions.")
        print("- Ensure the 'portfolio' table exists in your Supabase project.")

if __name__ == "__main__":
    verify()
