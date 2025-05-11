
import gradio as gr
import requests

def remote_generate(prompt, negative_prompt, width, height, steps):
    payload = {
        "prompt": prompt,
        "negative_prompt": negative_prompt,
        "width": width,
        "height": height,
        "steps": steps
    }
    try:
        response = requests.post("http://localhost:8000/generate", json=payload)
        response.raise_for_status()
        data = response.json()
        return data["image_url"]
    except Exception as e:
        return f"Erreur: {str(e)}"

with gr.Blocks() as demo:
    with gr.Row():
        prompt = gr.Textbox(label="Prompt")
        negative_prompt = gr.Textbox(label="Negative Prompt", value="")
    with gr.Row():
        width = gr.Slider(256, 2048, value=512, step=64, label="Width")
        height = gr.Slider(256, 2048, value=512, step=64, label="Height")
    with gr.Row():
        steps = gr.Slider(5, 50, value=20, step=1, label="Steps")
    with gr.Row():
        output = gr.Image(label="Result")

    run_btn = gr.Button("Generate")
    run_btn.click(fn=remote_generate,
                  inputs=[prompt, negative_prompt, width, height, steps],
                  outputs=[output])

demo.launch(server_name="0.0.0.0", server_port=7860)
