from fastapi import APIRouter, UploadFile, File
from PIL import Image
import torch
import torchvision.transforms as T
from backend.models.load_models import MODELS

router = APIRouter(prefix="/hide")

transform = T.Compose([
    T.Resize((128, 128)),
    T.ToTensor()
])

@router.post("/")
async def hide_api(cover: UploadFile = File(...), secret: UploadFile = File(...)):
    model = MODELS["stego"]
    if model is None:
        return {"error": "Model not loaded"}

    device = next(model.parameters()).device

    cover_img = Image.open(cover.file).convert("RGB")
    secret_img = Image.open(secret.file).convert("RGB")

    cover_t = transform(cover_img).unsqueeze(0).to(device)
    secret_t = transform(secret_img).unsqueeze(0).to(device)

    with torch.no_grad():
        stego, recovered = model(cover_t, secret_t)

    stego_np = (stego.squeeze().cpu().numpy().transpose(1, 2, 0) * 255).astype("uint8")

    return {"msg": "hide success", "shape": stego_np.shape}
