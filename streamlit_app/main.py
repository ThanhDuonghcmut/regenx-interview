import os
import requests
from datetime import datetime

import streamlit as st
from dotenv import load_dotenv
from supabase import create_client

DOTENV_PATH = ".env"
load_dotenv(DOTENV_PATH)
SECRET_KEY = os.environ.get("SUPABASE_API_KEY")

url = os.environ.get("SUPABASE_URL")
backend_url = os.environ.get("BACKEND_URL")

client = create_client(url, SECRET_KEY)

API_BASE = "https://<your-project-id>.functions.supabase.co"

# === State init ===
if 'token' not in st.session_state:
    st.session_state.token = None
if 'chat_state' not in st.session_state:
    st.session_state.chat_state = "login"
if 'collected' not in st.session_state:
    st.session_state.collected = {}

# === Auth UI ===
def auth_ui():
    st.title("🔐 Đăng nhập")
    email = st.text_input("Email")
    password = st.text_input("Mật khẩu", type="password")

    if st.button("Đăng nhập"):
        try:
            data = client.auth.sign_in_with_password({
                            'email': email,
                            'password': password,
                            })
            token = data.session.access_token
            st.session_state.token = token
            st.session_state.chat_state = "wait_image"
            st.success("🎉 Đăng nhập thành công!")
        except:
            st.error("Sai email hoặc mật khẩu!")

# === Gửi ảnh tới Edge Function để phân tích ===
def upload_image(image_bytes):
    res = requests.post(f"{backend_url}/image",
                        headers={"Authorization": f"Bearer {st.session_state.token}"},
                        files={"file": image_bytes})
    return res.json()

# === Gửi dữ liệu tới Edge Function để dự đoán ===
def upload_field_data(data):
    res = requests.post(f"{API_BASE}/field",
                        headers={"Authorization": f"Bearer {st.session_state.token}"},
                        json=data)
    return res.json()

# === Gửi kết quả về server ===
def save_prediction(data):
    res = requests.post(f"{API_BASE}/save_prediction",
                        headers={"Authorization": f"Bearer {st.session_state.token}"},
                        json=data)
    return res.status_code == 200


# === Main UI ===
def chatbot_ui():
    st.title("🤖 Chatbot Năng Suất Cà Phê")

    # if st.button("➕ Tạo cuộc trò chuyện mới"):
    #     st.session_state.chat_state = "quick_predict"
    #     st.session_state.collected = {}
    #     st.experimental_rerun()

    if st.session_state.chat_state == "wait_image":
        st.info("Vui lòng tải ảnh cây cà phê")
        image = st.file_uploader("Tải ảnh", type=["jpg", "png"])
        if image:
            info = upload_image(image)
            st.session_state.collected["forecast_id"] = info['forecast_id']
            
            if info["is_field_empty"]:
                st.session_state.chat_state = "ask_more_info"
            else:
                st.session_state.chat_state = "analyse"
            st.rerun()

    elif st.session_state.chat_state == "ask_more_info":
        try:
            area = st.text_input("Diện tích trồng (m²)")
            st.session_state.collected["area"] = float(area)
            count = st.text_input("Số lượng cây")
            st.session_state.collected["total_plants"] = int(count)
            location = st.text_input("Địa điểm trồng (VD: Lâm Đồng)")
            st.session_state.collected["location"] = location
            st.session_state.chat_state = "analyse"
            res = upload_field_data({"area": area, "total_plants": count, "location": location})
            print(res)
            st.rerun()
        except:
            st.error("Vui lòng nhập số hợp lệ")

    # elif st.session_state.chat_state == "quick_predict":
    #     st.info("Chỉ cần tải ảnh mới, hệ thống sẽ dùng dữ liệu cũ.")
    #     image = st.file_uploader("Tải ảnh mới", type=["jpg", "png"], key="quick_img")
    #     if image:
    #         with st.spinner("Phân tích ảnh..."):
    #             info = analyze_image(image)
    #             st.session_state.collected.update(info)
    #             last_data = get_last_data()
    #             if not last_data:
    #                 st.error("Không có dữ liệu cũ! Vui lòng dùng chế độ đầy đủ.")
    #                 st.session_state.chat_state = "wait_image"
    #                 return
    #             # Sử dụng dữ liệu cũ
    #             for k in ["area", "plant_count", "location", "temperature", "humidity", "rainfall", "predicted_yield", "timestamp"]:
    #                 if k in last_data:
    #                     st.session_state.collected[f"last_{k}" if k in ["predicted_yield", "timestamp"] else k] = last_data[k]
    #             result = predict_yield(st.session_state.collected)
    #             st.success(f"🌾 Năng suất mới: **{result['yield']} kg**")
    #             st.session_state.collected["predicted_yield"] = result["yield"]
    #             st.session_state.collected["timestamp"] = datetime.utcnow().isoformat()
    #             save_prediction(st.session_state.collected)

# === App Entry ===
if not st.session_state.token:
    auth_ui()
else:
    chatbot_ui()
