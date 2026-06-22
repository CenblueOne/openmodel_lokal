import gradio as gr
import anthropic
import os
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENMODEL_API_KEY")
if not API_KEY:
    raise ValueError("OPENMODEL_API_KEY environment variable not set")
client = anthropic.Anthropic(base_url="https://api.openmodel.ai", api_key=API_KEY)

# ==================== CUSTOM THEME ====================
custom_theme = gr.themes.Soft(
    primary_hue=gr.themes.colors.blue,
    secondary_hue=gr.themes.colors.slate,
    neutral_hue=gr.themes.colors.slate,
).set(
    button_primary_background_fill="#3b82f6",
    button_primary_background_fill_hover="#2563eb",
)

# ==================== MODEL LIST ====================
MODEL_CHOICES = [
    "deepseek-v4-flash",
    "deepseek-v4-pro",
    "claude-haiku-4-5-20251001",
    "claude-sonnet-4-6",
    "qwen3.6-flash",
    "qwen3.5-plus",
    "glm-5.2",
    "gemini-3.1-flash-lite-preview",
    "mimo-v2-flash",
    "kimi-k2.5",
]

# ==================== PRESETS ====================
PRESETS = {
    "General Assistant": "Kamu adalah asisten AI yang helpful, ramah, dan jawab dalam Bahasa Indonesia yang natural.",
    "Coding Assistant": "Kamu adalah programmer senior. Jawab dengan kode yang bersih dan penjelasan jelas.",
    "Stock Trading Analyst": "Kamu adalah analis saham IDX. Jawab data-driven dan fokus pada peluang trading.",
    "AHSP Construction": "Kamu adalah ahli AHSP konstruksi SDA & BM sesuai regulasi 2026.",
    "Creative Writer": "Kamu adalah penulis kreatif dalam Bahasa Indonesia.",
}

def chat_fn(message, history, model, max_tokens, temperature, system_prompt):
    messages = []
    for h in history:
        messages.append({"role": h["role"], "content": h["content"]})
    messages.append({"role": "user", "content": message})

    try:
        full_response = ""
        with client.messages.stream(
            model=model,
            max_tokens=int(max_tokens),
            temperature=float(temperature),
            system=system_prompt.strip() if system_prompt.strip() else None,
            messages=messages,
        ) as stream:
            for event in stream:
                if event.type == "content_block_delta":
                    if hasattr(event.delta, "text"):
                        full_response += event.delta.text
                        yield full_response
    except Exception as e:
        yield f"❌ Error: {str(e)}"

def apply_preset(preset_name):
    return PRESETS.get(preset_name, "")

def save_history(history_list):
    if not history_list:
        return "History kosong."
    filename = f"chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(history_list, f, ensure_ascii=False, indent=2)
    return f"✅ Saved: {filename}"

def export_chat(history_list):
    if not history_list:
        return None
    lines = [f"[{m['role'].capitalize()}]\n{m['content']}\n" for m in history_list]
    filename = f"chat_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return filename

# ==================== UI ====================
with gr.Blocks(title="OpenModel.ai Chat") as demo:  # Hapus theme dari sini
    gr.Markdown("# 🤖 OpenModel.ai Chat\n### Streaming + Model Dropdown + Presets + History")

    with gr.Row():
        with gr.Column(scale=1, min_width=300):
            gr.Markdown("### ⚙️ Model Settings")
            model = gr.Dropdown(
                choices=MODEL_CHOICES,
                value="deepseek-v4-flash",
                label="Model",
                allow_custom_value=True,
                info="Pilih dari daftar atau ketik manual"
            )
            max_tokens = gr.Slider(256, 8192, step=256, value=2048, label="Max Tokens")
            temperature = gr.Slider(0.0, 1.0, step=0.1, value=0.7, label="Temperature")

            gr.Markdown("### 🎯 System Prompt")
            preset = gr.Dropdown(list(PRESETS.keys()), value="General Assistant", label="Preset")
            system_prompt = gr.Textbox(label="System Prompt", value=PRESETS["General Assistant"], lines=5)
            preset.change(apply_preset, preset, system_prompt)

            gr.Markdown("### 💾 History")
            with gr.Row():
                save_btn = gr.Button("💾 Save JSON", variant="secondary")
                export_btn = gr.Button("📤 Export .txt", variant="secondary")
            status = gr.Textbox(label="Status", interactive=False)

            gr.Markdown("---")
            gr.Markdown("<small>Free DeepSeek • OpenModel.ai • Gradio 6</small>")

        with gr.Column(scale=4):
            chat = gr.ChatInterface(
                fn=chat_fn,
                additional_inputs=[model, max_tokens, temperature, system_prompt],
                title="DeepSeek Chat (Free)",
                description="Model dropdown dari openmodel.ai/model-pricing",
            )
            clear_btn = gr.Button("🗑️ Clear Chat", variant="stop")
            clear_btn.click(fn=lambda: [], inputs=None, outputs=chat.chatbot)

    save_btn.click(fn=save_history, inputs=chat.chatbot, outputs=status)
    export_btn.click(fn=export_chat, inputs=chat.chatbot, outputs=status)

    gr.Markdown("<small>Powered by OpenModel.ai • Anthropic SDK</small>")
    
if __name__ == "__main__":
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,           # ganti port agar tidak bentrok dengan yang lain
        inbrowser=True,             # otomatis buka browser
        theme=custom_theme          # pindahkan theme ke sini (Gradio 6.0+)
    )