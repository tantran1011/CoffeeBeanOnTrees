import google.generativeai as genai
import os
from services.weather import get_weather
from services.interference import pred_img
from services.auth import verify_token
from dotenv import load_dotenv
from datetime import datetime
from supabase import create_client, Client
import uuid

load_dotenv()

# Initialize configurations
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(url, key)
genai.configure(api_key=os.getenv("CHATBOT_API"))
model = genai.GenerativeModel('gemini-2.0-flash')


def upload_image_to_supabase(image_bytes: bytes, user_id: str) -> str:
    """Upload image to Supabase Storage and return public URL"""
    file_name = f"{user_id}/{uuid.uuid4()}.jpg"
    res = supabase.storage.from_("chatbot-images").upload(file_name, image_bytes, {"content-type": "image/jpeg"})
    
    if res.get("error"):
        raise Exception(res["error"]["message"])
    
    # Tạo URL
    public_url = f"{url}/storage/v1/object/public/chatbot-images/{file_name}"
    return public_url


def get_session_state(session_id: str) -> dict:
    """Retrieve or initialize session state from database"""
    res = supabase.table("conversation_state").select("*").eq("session_id", session_id).execute()
    
    if res.data:
        return res.data[0]
    else:
        # New session
        default_state = {
            "session_id": session_id,
            "step": 0,
            "image_comment": None,
            "num_trees": None,
            "area_hectares": None,
            "location": None,
            "weather_info": None,
            "final_yield_estimation": None,
            "updated_at": datetime.now().isoformat(),
        }
        supabase.table("conversation_state").insert(default_state).execute()
        return default_state


def update_session_state(session_id: str, updates: dict):
    """Update session state in database"""
    updates["updated_at"] = datetime.now().isoformat()
    supabase.table("conversation_state").update(updates).eq("session_id", session_id).execute()


def next_bot_messages(session_id: str, user_input: str, image: str = None, access_token: str = None) -> str:

    # Check Auth
    user_id = verify_token(access_token)
    if not user_id:
        return "Bạn chưa đăng nhập hoặc token không hợp lệ."

    if session_id != user_id:
        return "Phiên không hợp lệ. Hãy đăng nhập lại."


    """Handle conversation flow based on current step"""
    state = get_session_state(session_id)
    step = state["step"]

    # Step 0: Analyze Image
    if step == 0 and image:
        coffee_beans_status = pred_img(image)
        total_beans = sum(coffee_beans_status.values())
        response = model.generate_content(
            f"Hãy nhận xét tình trạng cây cà phê sau: {coffee_beans_status} trên tổng cộng {total_beans}"
        )
        
        reply = response.text
        update_session_state(session_id, {"step": 1, "image_comment": reply})
        return f"{reply}.\nĐể phân tích chính xác hơn, bạn hãy cho tôi biết về số lượng cây của bạn ?"

    # Step 1: Ask number of trees
    if step == 1:
        update_session_state(session_id, {"step": 2, "num_trees": user_input})
        return f"Cảm ơn. Trang trại của bạn có {user_input} cây cà phê.\nDiện tích là bao nhiêu héc-ta?"

    # Step 2: Ask area
    if step == 2:
        update_session_state(session_id, {"step": 3, "area_hectares": user_input})
        return f"Trang trại diện tích {user_input} héc-ta. Bạn ở tỉnh/thành nào?"

    # Step 3: Ask Location and yield_calc
    if step == 3:
        update_session_state(session_id, {"step": 4, "location": user_input})
        weather = get_weather(user_input)
        update_session_state(session_id, {"weather_info": weather})

        # Generate yield
        prompt = (
            f"Dựa trên thông tin sau: \n"
            f"- Tình trạng cây: {state['image_comment']}\n"
            f"- Số cây: {state['num_trees']}\n"
            f"- Diện tích: {state['area_hectares']} héc-ta\n"
            f"- Địa điểm: {user_input}\n"
            f"- Thời tiết: {weather}\n"
            f"Hãy đánh giá năng suất tiềm năng (kg/héc-ta) và đưa ra lời khuyên chăm sóc."
        )
        response = model.generate_content(prompt)
        update_session_state(session_id, {"step": 5, "final_yield_estimation": response.text})

        # Add to table conversation_history
        supabase.table("conversation_history").insert({
        "user_id": session_id,
        "image_comment": state['image_comment'],
        "num_trees": state['num_trees'],
        "area_hectares": state['area_hectares'],
        "location": user_input,
        "weather_info": weather,
        "final_yield_estimation": response.text,
        }).execute()

        return (
            f"Thời tiết tại {user_input} hiện là: {weather}.\n\n"
            f"🌾 Ước tính năng suất:\n{response.text}"
        )
