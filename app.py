import streamlit as st
import pygame
import random
import numpy as np
from PIL import Image
import time

# Cấu hình trang Streamlit
st.set_page_config(page_title="Flappy Bird Streamlit", page_icon="🐦", layout="centered")

st.title("🐦 Flappy Bird (Streamlit Edition)")
st.caption("Nhấn nút 'Bay lên!' hoặc 'Bắt đầu' để chơi.")

# Kích thước màn hình game
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
GRAVITY = 0.4
FLAP_STRENGTH = -7
PIPE_SPEED = 4
PIPE_GAP = 160

# Khởi tạo trạng thái ứng dụng (Session State)
if "game_running" not in st.session_state:
    st.session_state.game_running = False
if "score" not in st.session_state:
    st.session_state.score = 0
if "high_score" not in st.session_state:
    st.session_state.high_score = 0
if "bird_y" not in st.session_state:
    st.session_state.bird_y = SCREEN_HEIGHT // 2
if "bird_velocity" not in st.session_state:
    st.session_state.bird_velocity = 0
if "pipes" not in st.session_state:
    st.session_state.pipes = []
if "last_pipe" not in st.session_state:
    st.session_state.last_pipe = time.time()

def reset_game():
    st.session_state.bird_y = SCREEN_HEIGHT // 2
    st.session_state.bird_velocity = 0
    st.session_state.pipes = []
    st.session_state.score = 0
    st.session_state.game_running = True
    st.session_state.last_pipe = time.time()

def flap():
    if st.session_state.game_running:
        st.session_state.bird_velocity = FLAP_STRENGTH

# Giao diện điều khiển nút bấm
col1, col2 = st.columns(2)
with col1:
    if st.button("🚀 Bắt đầu / Chơi lại", use_container_width=True):
        reset_game()
with col2:
    if st.button("🪽 Bay lên!", use_container_width=True):
        flap()

# Khai báo khung hiển thị hình ảnh game và điểm số
game_image_place = st.empty()
score_place = st.empty()

# Khởi tạo Pygame ở chế độ không mở cửa sổ (Headless)
pygame.init()
surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

# Vòng lặp cập nhật Game
if st.session_state.game_running:
    # 1. Cập nhật vị trí Chim
    st.session_state.bird_velocity += GRAVITY
    st.session_state.bird_y += st.session_state.bird_velocity

    # 2. Tạo Cột mới
    current_time = time.time()
    if current_time - st.session_state.last_pipe > 1.4:
        top_height = random.randint(60, SCREEN_HEIGHT - PIPE_GAP - 120)
        st.session_state.pipes.append({
            "x": SCREEN_WIDTH,
            "top": top_height,
            "bottom": top_height + PIPE_GAP,
            "passed": False
        })
        st.session_state.last_pipe = current_time

    # 3. Cập nhật Cột & Tính điểm
    new_pipes = []
    for pipe in st.session_state.pipes:
        pipe["x"] -= PIPE_SPEED
        if pipe["x"] + 60 > 0:
            new_pipes.append(pipe)
        
        if not pipe["passed"] and pipe["x"] < 100:
            st.session_state.score += 1
            pipe["passed"] = True
            if st.session_state.score > st.session_state.high_score:
                st.session_state.high_score = st.session_state.score

    st.session_state.pipes = new_pipes

    # 4. Kiểm tra Va chạm
    bird_rect = pygame.Rect(100, int(st.session_state.bird_y), 30, 30)
    
    # Chạm trần hoặc sàn
    if st.session_state.bird_y <= 0 or st.session_state.bird_y >= SCREEN_HEIGHT - 30:
        st.session_state.game_running = False

    # Chạm cột
    for pipe in st.session_state.pipes:
        top_pipe_rect = pygame.Rect(pipe["x"], 0, 60, pipe["top"])
        bottom_pipe_rect = pygame.Rect(pipe["x"], pipe["bottom"], 60, SCREEN_HEIGHT - pipe["bottom"])
        if bird_rect.colliderect(top_pipe_rect) or bird_rect.colliderect(bottom_pipe_rect):
            st.session_state.game_running = False

    # 5. Vẽ Game lên Pygame Surface
    surface.fill((135, 206, 235))  # Nền trời xanh

    # Vẽ Chim
    pygame.draw.circle(surface, (255, 255, 0), (115, int(st.session_state.bird_y) + 15), 15)

    # Vẽ Cột
    for pipe in st.session_state.pipes:
        pygame.draw.rect(surface, (34, 139, 34), (pipe["x"], 0, 60, pipe["top"]))
        pygame.draw.rect(surface, (34, 139, 34), (pipe["x"], pipe["bottom"], 60, SCREEN_HEIGHT - pipe["bottom"]))

    # Chuyển đổi Pygame Surface thành Image để Streamlit hiển thị
    img_data = pygame.surfarray.array3d(surface)
    img_data = np.transpose(img_data, (1, 0, 2))
    img = Image.fromarray(img_data)
    
    game_image_place.image(img, use_column_width=True)
    score_place.markdown(f"### 🏆 Điểm hiện tại: **{st.session_state.score}** | 🥇 Kỷ lục: **{st.session_state.high_score}**")
    
    # Tạm dừng ngắn để tạo khung hình mượt mà và tự động gọi lại app
    time.sleep(0.025)
    st.rerun()

else:
    # Hiển thị màn hình chờ / Kết thúc
    surface.fill((135, 206, 235))
    pygame.draw.circle(surface, (255, 255, 0), (115, SCREEN_HEIGHT // 2), 15)
    
    # Vẽ các cột mẫu nền
    pygame.draw.rect(surface, (34, 139, 34), (250, 0, 60, 200))
    pygame.draw.rect(surface, (34, 139, 34), (250, 360, 60, 240))

    img_data = pygame.surfarray.array3d(surface)
    img_data = np.transpose(img_data, (1, 0, 2))
    img = Image.fromarray(img_data)
    
    game_image_place.image(img, use_column_width=True)
    
    if st.session_state.score > 0:
        score_place.markdown(f"### 💥 Thua rồi! Điểm của bạn: **{st.session_state.score}** | 🥇 Kỷ lục: **{st.session_state.high_score}**")
    else:
        score_place.markdown(f"### 🎮 Bấm **🚀 Bắt đầu / Chơi lại** để bắt đầu! | 🥇 Kỷ lục: **{st.session_state.high_score}**")
