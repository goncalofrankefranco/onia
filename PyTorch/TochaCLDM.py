import os
import torch
import numpy as np
from PIL import Image
from diffusers import StableDiffusionControlNetPipeline, ControlNetModel,UniPCMultistepScheduler
from inspect import signature

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
# Configure HF_TOKEN in the environment before running this script.

canvas = np.zeros((256, 256, 3), dtype=np.uint8)
canvas[110:146, 40:216] = [255, 255, 255] # Mimics hard line condition
condition_image = Image.fromarray(canvas) # NumPy -> PIL

# Controls pretrained large diffusion models to support additional input conditions
controlnet = ControlNetModel.from_pretrained(
    "lllyasviel/sd-controlnet-canny",
    torch_dtype=torch.float32
)

pipeline = StableDiffusionControlNetPipeline.from_pretrained(
    "InternationalOlympiadAI/miniSD-diffusers",
    controlnet=controlnet,
    torch_dtype=torch.float32
)

pipeline.safety_checker = None
pipeline.feature_extractor = None
pipeline.requires_safety_checker = False
pipeline.vae.config.shift_factor = 0.18215 # Converts VAE numbers range to MiniSD numbers range

# OPTIMIZATIONS
pipeline.scheduler = UniPCMultistepScheduler.from_config(pipeline.scheduler.config) # Drop sampling loops to 15-20 steps
pipeline.enable_model_cpu_offload() # Accelerator = GPU. Splits memory between VRAM and RAM

print(signature(pipeline))
prompt = input("Escreva um prompt: ")
output = pipeline(
    prompt=prompt,
    image=condition_image,
    num_inference_steps=20,
    height=256,
    width=256
)

final_image = output.images[0]
final_image.save("foto_mt_legal.png")
