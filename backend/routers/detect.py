from fastapi import APIRouter, UploadFile, File
import torch
import torchvision.transforms as T
from PIL import Image
from backend.models.load_models import MODELS

router = APIRouter(prefix="/detect")

transform = T.Compose([
    T.Resize((128, 128)),
    T.ToTensor()
])

@router.post("/")
async def detect_api(file: UploadFile = File(...)):
    model = MODELS["detect"]
    if model is None:
        return {"error": "Model not loaded"}

    img = Image.open(file.file).convert("RGB")
    x = transform(img).unsqueeze(0)

    device = next(model.parameters()).device
    x = x.to(device)

    with torch.no_grad():
        out = model(x)

    pred = out.argmax(1).item()
    label = "stego" if pred == 1 else "clean"

    return {"prediction": label}
