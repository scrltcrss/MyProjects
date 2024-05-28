from flask import Flask, render_template, request, send_file, url_for
from diffusers import DiffusionPipeline
import torch
from io import BytesIO
import os

app = Flask(__name__)

def load_pipelines():
    base = DiffusionPipeline.from_pretrained(
        "stabilityai/stable-diffusion-xl-base-1.0",
        torch_dtype=torch.float16,
        use_safetensors=True,
        variant="fp16"
    )
    refiner = DiffusionPipeline.from_pretrained(
        "stabilityai/stable-diffusion-xl-refiner-1.0",
        text_encoder_2=base.text_encoder_2,
        vae=base.vae,
        torch_dtype=torch.float16,
        use_safetensors=True,
        variant="fp16"
    )
    return base.to(device), refiner.to(device)

device = "cuda" if torch.cuda.is_available() else "cpu"
base, refiner = load_pipelines()

def generate_image(prompt, base, refiner, n_steps=40, high_noise_frac=0.8):
    with torch.no_grad():
        image = base(prompt=prompt, num_inference_steps=n_steps, denoising_end=high_noise_frac, output_type="latent").images
        image = refiner(prompt=prompt, num_inference_steps=n_steps, denoising_start=high_noise_frac, image=image).images[0]
    return image

@app.route("/", methods=["GET", "POST"])
def index():
    image_url = None
    if request.method == "POST":
        prompt = request.form["prompt"]
        try:
            image = generate_image(prompt, base, refiner)
            img_io = BytesIO()
            image.save(img_io, 'PNG')
            img_io.seek(0)
            image_path = os.path.join('static', 'generated_image.png')
            with open(image_path, 'wb') as f:
                f.write(img_io.getbuffer())
            image_url = url_for('static', filename='generated_image.png')
        except Exception as e:
            return f"Error: {e}"
    return render_template("index.html", image_url=image_url)

if __name__ == "__main__":
    app.run(debug=True)