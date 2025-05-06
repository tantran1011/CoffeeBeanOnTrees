import streamlit as st
from services.auth import signup, login
from services.yield_calc import next_bot_messages, get_session_state, update_session_state, upload_image_to_supabase, update_conversation_image
import base64

st.set_page_config(page_title="Dự đoán năng suất cà phê", page_icon="🌱")

# Lưu trạng thái người dùng
if "access_token" not in st.session_state:
    st.session_state.access_token = None
    st.session_state.user_id = None
    st.session_state.logged_in = False
    st.session_state.chat_started = False

st.title("🌱 Coffee Yield Chatbot")
st.markdown("Hệ thống dự đoán năng suất cà phê qua ảnh và thông tin nông trại.")

# ============ LOGIN & SIGNUP ============
auth_tab = st.sidebar.radio("🔐 Tài khoản", ["Đăng nhập", "Đăng ký"])

if not st.session_state.logged_in:
    with st.sidebar.form("auth_form"):
        email = st.text_input("Email")
        password = st.text_input("Mật khẩu", type="password")
        full_name = None

        if auth_tab == "Đăng ký":
            full_name = st.text_input("Họ tên")

        submitted = st.form_submit_button("Gửi")
        if submitted:
            if auth_tab == "Đăng nhập":
                result = login(email, password)
                if "error" in result:
                    st.sidebar.error("❌ " + result["error"])
                else:
                    st.session_state.access_token = result["access_token"]
                    st.session_state.user_id = result["user_id"]
                    st.session_state.logged_in = True
                    st.sidebar.success("✅ Đăng nhập thành công!")
            else:
                result = signup(email, password, full_name)
                if "error" in result:
                    st.sidebar.error("❌ " + result["error"])
                else:
                    st.sidebar.success("✅ Đăng ký thành công! Hãy đăng nhập.")
else:
    st.sidebar.success("🟢 Đã đăng nhập!")
    if st.sidebar.button("Đăng xuất"):
        st.session_state.logged_in = False
        st.session_state.access_token = None
        st.session_state.user_id = None
        st.session_state.chat_started = False
        st.rerun()


# ============ CHATBOT UI ============

if st.session_state.logged_in:
    st.header("🤖 Trò chuyện với chatbot")

    if not st.session_state.chat_started:
        st.subheader("1️⃣ Gửi ảnh cây cà phê")
        uploaded_file = st.file_uploader("Chọn ảnh cây cà phê", type=["jpg", "jpeg", "png"])
        
        if uploaded_file:
            image_bytes = uploaded_file.getvalue()
            
            image_url = upload_image_to_supabase(image_bytes, user_id=st.session_state.user_id)
            update_conversation_image(user_id=st.session_state.user_id, image_url=image_url)

            image_base64 = base64.b64encode(image_bytes).decode("utf-8")

            bot_reply = next_bot_messages(
                session_id=st.session_state.user_id,
                user_input="",
                image=image_base64,
                access_token=st.session_state.access_token
            )

            st.session_state.chat_started = True
            st.session_state.last_bot_msg = bot_reply
            st.image(image_bytes, caption="Ảnh đã gửi", use_container_width=True)
            st.success(bot_reply)
            st.rerun()

    else:
        st.subheader("💬 Tiếp tục trả lời câu hỏi")
        st.info(st.session_state.last_bot_msg)

        # Kiểm tra nếu cuộc hội thoại đã hoàn tất
        state = get_session_state(st.session_state.user_id)
        if state["step"] == 5:
            st.success("🎉 Cuộc hội thoại đã hoàn tất.")
            if st.button("🔄 Bắt đầu lại"):
                update_session_state(st.session_state.user_id, {
                    "step": 0,
                    "image_comment": None,
                    "num_trees": None,
                    "area_hectares": None,
                    "location": None,
                    "weather_info": None,
                    "final_yield_estimation": None
                })
                st.session_state.chat_started = False
                st.rerun()

        with st.form("chat_form"):
            user_input = st.text_input("✍️ Nhập câu trả lời")
            submitted = st.form_submit_button("Gửi")
            if submitted and user_input.strip():
                with st.spinner("🤖 Đang phân tích dữ liệu, vui lòng chờ..."):
                    bot_reply = next_bot_messages(
                        session_id=st.session_state.user_id,
                        user_input=user_input,
                        access_token=st.session_state.access_token
                    )
                st.session_state.last_bot_msg = bot_reply
                st.success(bot_reply)
