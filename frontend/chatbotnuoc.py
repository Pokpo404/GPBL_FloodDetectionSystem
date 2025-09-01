import gradio as gr
import matplotlib.pyplot as plt
import random

# Hàm chatbot (format mới: type="messages")
def chatbot(user_input, history):
    if "mực nước" in user_input.lower():
        response = "💧 Hiện tại mực nước trung bình là **1.2m** → An toàn ✅"
    elif "cảnh báo" in user_input.lower():
        response = "⚠️ Cảnh báo: Nguy cơ ngập ở khu vực thấp!"
    else:
        response = "🤖 Bạn có thể hỏi về: **mực nước**, **cảnh báo**, hoặc **thời tiết**."

    history = history + [
        {"role": "user", "content": user_input},
        {"role": "assistant", "content": response},
    ]
    return history, history

# Hàm vẽ biểu đồ mực nước (giả lập dữ liệu 7 ngày)
def plot_water_level():
    days = list(range(1, 8))
    water_levels = [random.uniform(0.8, 2.5) for _ in days]

    plt.figure(figsize=(6,4))
    plt.plot(days, water_levels, marker='o', color="blue")
    plt.title("📊 Biểu đồ mực nước 7 ngày gần nhất", fontsize=14)
    plt.xlabel("Ngày")
    plt.ylabel("Mực nước (m)")
    plt.grid(True)
    return plt

with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown(
        """
        # 🌊 Trợ lý cảnh báo lũ
        Xin chào! Tôi sẽ cung cấp thông tin về **mực nước, cảnh báo ngập lụt** và hỗ trợ bạn theo dõi tình hình.
        """
    )

    with gr.Row():
        with gr.Column(scale=2):
            gr.Markdown("### 💬 Chatbot hỗ trợ")
            chatbot_ui = gr.Chatbot(type="messages", height=400)
            msg = gr.Textbox(placeholder="Nhập câu hỏi của bạn và nhấn Enter...", show_label=False)
            with gr.Row():
                clear = gr.Button("🗑️ Xóa hội thoại", variant="secondary")

        with gr.Column(scale=1):
            gr.Markdown("### 📊 Biểu đồ mực nước")
            plot_output = gr.Plot()

    # Kết nối sự kiện chatbot
    msg.submit(chatbot, [msg, chatbot_ui], [chatbot_ui, chatbot_ui], queue=False).then(
        lambda: "", None, msg
    )
    clear.click(lambda: [], None, chatbot_ui, queue=False)

    # Auto update biểu đồ mỗi 5 giây
    demo.load(
        fn=plot_water_level,
        inputs=None,
        outputs=plot_output  # Gradio 4.x chuẩn
    )

demo.launch()
