from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(url, key)

def signup(email: str, password: str, full_name:str):
    result = supabase.auth.sign_up({
        "email": email,
        "password": password,
    })


    user = result.user
    if not user:
        return {"error": "Signup failed"}

    # Thêm vào bảng users (nếu cần)
    supabase.table("profiles").insert({
        "id": user.id,
        "email": email,
        "full_name": full_name,
        "role": "farmer"
    }).execute()

    return {"message": "Signup successful", "user_id": user.id}


def login(email: str, password: str):
    try:
        result = supabase.auth.sign_in_with_password({
        "email": email,
        "password": password
        })


        if result.session:
            return {
                "access_token": result.session.access_token,
                "user_id": result.user.id
            }
        else:
            return {"error": "Login failed"}
    except Exception as e:
        return {"error": str(e)}

def verify_token(access_token: str):
    try:
        user = supabase.auth.get_user(access_token)
        return user.user.id if user.user else None
    except Exception as e:
        print(f"Token verification error: {e}")
        return None
