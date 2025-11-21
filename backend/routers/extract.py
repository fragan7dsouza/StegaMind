from fastapi import APIRouter, UploadFile, File
import torch
import torchvision.transforms as T
from PIL import Image
import numpy as np
from backend.models.load_models import MODELS

router = APIRouter(prefix="/extract")

t = T.Compose([
    T.Resize((128, 128)),
    T.ToTensor()
])

def to_tensor(file):
    img = Image.open(file).convert("RGB")
    return t(img).unsqueeze(0)

def to_image(tensor):
    arr = tensor.squeeze().detach().cpu().numpy().transpose(1, 2, 0)
    arr = np.clip(arr * 255, 0, 255).astype("uint8")
    return Image.fromarray(arr)

@router.post("/")
async def extract_api(stego: UploadFile = File(...)):
    model = MODELS["stego"]
    if model is None:
        return {"error": "Model not loaded"}

    device = next(model.parameters()).device
    stego_t = to_tensor(stego.file).to(device)

    with torch.no_grad():
        _, recovered = model(stego_t, stego_t)

    out_img = to_image(recovered)
    out_path = "backend_output_recovered.png"
    out_img.save(out_path)

    return {"saved": out_path}
