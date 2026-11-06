import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Flappy Bird Streamlit", page_icon="🐦", layout="centered"
)

st.title("🐦 Flappy Bird Game")
st.caption(
    "Nhấn nút **Bay lên** bên dưới hoặc phím **SPACE** (Khoảng trống) trên bàn"
    " phím để điều khiển chim!"
)

# Mã nguồn HTML, CSS và JavaScript của game Flappy Bird
game_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body {
            margin: 0;
            padding: 0;
            background-color: #70c5ce;
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
            font-family: sans-serif;
        }
        canvas {
            border: 2px solid #000;
            background-color: #70c5ce;
            box-shadow: 0px 4px 10px rgba(0,0,0,0.3);
        }
        .btn-container {
            margin-top: 15px;
        }
        .jump-btn {
            background-color: #ff9800;
            color: white;
            border: none;
            padding: 12px 30px;
            font-size: 18px;
            font-weight: bold;
            border-radius: 8px;
            cursor: pointer;
            box-shadow: 0 4px #e65100;
        }
        .jump-btn:active {
            box-shadow: 0 2px #e65100;
            transform: translateY(2px);
        }
    </style>
</head>
<body>

    <canvas id="canvas" width="320" height="480"></canvas>
    
    <div class="btn-container">
        <button class="jump-btn" onclick="flap()">BAY LÊN 🚀</button>
    </div>

    <script>
        const cvs = document.getElementById("canvas");
        const ctx = cvs.getContext("2d");

        // Biến điều khiển game
        let birdX = 50;
        let birdY = 150;
        let gravity = 0.35;
        let velocity = 0;
        let jump = -6.5;
        let score = 0;
        let gameOver = false;

        const pipeWidth = 50;
        const pipeGap = 125;
        let pipes = [];

        // Thêm cột ban đầu
        pipes[0] = {
            x: cvs.width,
            top: Math.floor(Math.random() * (cvs.height - pipeGap - 100)) + 30
        };

        // Bắt sự kiện bàn phím (Phím Space)
        document.addEventListener("keydown", function(e) {
            if (e.code === "Space") {
                flap();
            }
        });

        function flap() {
            if (gameOver) {
                resetGame();
            } else {
                velocity = jump;
            }
        }

        function resetGame() {
            birdY = 150;
            velocity = 0;
            score = 0;
            pipes = [];
            pipes[0] = {
                x: cvs.width,
                top: Math.floor(Math.random() * (cvs.height - pipeGap - 100)) + 30
            };
            gameOver = false;
            draw();
        }

        function draw() {
            // 1. Nền bầu trời
            ctx.fillStyle = "#70c5ce";
            ctx.fillRect(0, 0, cvs.width, cvs.height);

            // 2. Vẽ các cột ống
            for (let i = 0; i < pipes.length; i++) {
                ctx.fillStyle = "#73bf2e";
                ctx.strokeStyle = "#53801b";
                ctx.lineWidth = 2;

                // Ống trên
                ctx.fillRect(pipes[i].x, 0, pipeWidth, pipes[i].top);
                ctx.strokeRect(pipes[i].x, 0, pipeWidth, pipes[i].top);

                // Ống dưới
                let bottomPipeY = pipes[i].top + pipeGap;
                let bottomPipeHeight = cvs.height - bottomPipeY - 20;
                ctx.fillRect(pipes[i].x, bottomPipeY, pipeWidth, bottomPipeHeight);
                ctx.strokeRect(pipes[i].x, bottomPipeY, pipeWidth, bottomPipeHeight);

                // Di chuyển cột sang trái
                if (!gameOver) {
                    pipes[i].x -= 2;
                }

                // Thêm cột mới khi cột cũ sang giữa màn hình
                if (pipes[i].x === 140) {
                    pipes.push({
                        x: cvs.width,
                        top: Math.floor(Math.random() * (cvs.height - pipeGap - 100)) + 30
                    });
                }

                // Xử lý va chạm
                if (birdX + 15 > pipes[i].x && birdX - 15 < pipes[i].x + pipeWidth) {
                    if (birdY - 15 < pipes[i].top || birdY + 15 > bottomPipeY) {
                        gameOver = true;
                    }
                }

                // Tăng điểm khi vượt qua cột
                if (pipes[i].x === 48 && !gameOver) {
                    score++;
                }
            }

            // Xóa các cột đã đi ra khỏi màn hình
            if (pipes.length > 0 && pipes[0].x < -pipeWidth) {
                pipes.shift();
            }

            // 3. Mặt đất
            ctx.fillStyle = "#ded895";
            ctx.fillRect(0, cvs.height - 20, cvs.width, 20);
            ctx.fillStyle = "#73bf2e";
            ctx.fillRect(0, cvs.height - 20, cvs.width, 4);

            // 4. Chim (Flappy Bird)
            ctx.beginPath();
            ctx.arc(birdX, birdY, 13, 0, Math.PI * 2);
            ctx.fillStyle = "#f4c430";
            ctx.fill();
            ctx.lineWidth = 2;
            ctx.strokeStyle = "#000";
            ctx.stroke();

            // Mắt chim
            ctx.beginPath();
            ctx.arc(birdX + 5, birdY - 4, 3, 0, Math.PI * 2);
            ctx.fillStyle = "#fff";
            ctx.fill();
            ctx.beginPath();
            ctx.arc(birdX + 6, birdY - 4, 1.5, 0, Math.PI * 2);
            ctx.fillStyle = "#000";
            ctx.fill();

            // Mỏ chim
            ctx.fillStyle = "#ff5722";
            ctx.fillRect(birdX + 8, birdY, 8, 5);

            // 5. Cập nhật trọng lực chim
            if (!gameOver) {
                velocity += gravity;
                birdY += velocity;
            }

            // Kiểm tra chạm sàn hoặc trần
            if (birdY + 13 >= cvs.height - 20 || birdY - 13 <= 0) {
                gameOver = true;
            }

            // 6. Hiển thị Điểm số
            ctx.fillStyle = "#FFF";
            ctx.strokeStyle = "#000";
            ctx.lineWidth = 3;
            ctx.font = "bold 35px sans-serif";
            ctx.strokeText(score, cvs.width / 2 - 10, 50);
            ctx.fillText(score, cvs.width / 2 - 10, 50);

            // 7. Màn hình Game Over
            if (gameOver) {
                ctx.fillStyle = "rgba(0, 0, 0, 0.5)";
                ctx.fillRect(0, 0, cvs.width, cvs.height);

                ctx.fillStyle = "#FFF";
                ctx.font = "bold 26px sans-serif";
                ctx.textAlign = "center";
                ctx.fillText("GAME OVER", cvs.width / 2, cvs.height / 2 - 10);
                
                ctx.font = "16px sans-serif";
                ctx.fillText("Bấm BAY LÊN để chơi lại", cvs.width / 2, cvs.height / 2 + 25);
            }

            requestAnimationFrame(draw);
        }

        draw();
    </script>
</body>
</html>
"""

# Nhúng game HTML vào ứng dụng Streamlit
components.html(game_html, height=580)
