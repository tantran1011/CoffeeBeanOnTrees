from services.yield_calc import next_bot_messages
from services.auth import login
import base64
from config.config import img_test


# Đăng nhập để lấy token
result = login("tantranthongtin@gmail.com", "123456")
token = result["access_token"]
user_id = result["user_id"]

# Đổi img sang base64 để test
with open(img_test, "rb") as image_file:
    image_base64 = base64.b64encode(image_file.read()).decode('utf-8')

# Bắt đầu chat
print(next_bot_messages(user_id, "", image=image_base64, access_token=token))
print(next_bot_messages(user_id, "500", access_token=token))  # nhập số cây
print(next_bot_messages(user_id, "2", access_token=token))    # nhập diện tích (héc-ta)
print(next_bot_messages(user_id, "Hanoi", access_token=token))  # nhập địa điểm
