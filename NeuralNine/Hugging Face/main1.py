from diffusers import StableDiffusionPipeline
import torch

# Model Stable Diffusion
model_id = "sd-legacy/stable-diffusion-v1-5"

# On CPU, use float32
pipe = StableDiffusionPipeline.from_pretrained(
    model_id,
    torch_dtype=torch.float32
)

# Use cpu
pipe = pipe.to("cpu")

# Prompt
prompt = "a photo of an astronaut riding a horse on Mars"

# Generation
image = pipe(prompt).images[0]

# Save
image.save("astronaut_rides_horse.png")

print("Image create with sucess !")

