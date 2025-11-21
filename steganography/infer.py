import torch
import torchvision.transforms as T
from PIL import Image
import numpy as np
from steganography.model import StegoAutoencoder
from utils.metrics import psnr, ssim

transform = T.Compose([
    T.Resize((128, 128)),
    T.ToTensor()
])

def load_image(path):
    return transform(Image.open(path).convert("RGB")).unsqueeze(0)

def save_image(tensor, path):
    img = tensor.squeeze(0).detach().cpu().numpy().transpose(1, 2, 0)
    img = np.clip(img * 255, 0, 255).astype("uint8")
    Image.fromarray(img).save(path)

# ---------------------------------------------------------
# HIDE: embeds secret into cover image
# ---------------------------------------------------------
def hide(cover_path, secret_path, out_path, model_path):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = StegoAutoencoder(device=device)
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.eval()

    cover = load_image(cover_path).to(device)
    secret = load_image(secret_path).to(device)

    with torch.no_grad():
        stego, recovered = model(cover, secret)

    save_image(stego, out_path)
    save_image(recovered, out_path.replace(".png", "_recovered.png"))

    c = cover.squeeze().permute(1, 2, 0).cpu().numpy()
    s = stego.squeeze().permute(1, 2, 0).cpu().numpy()

    print(f"psnr: {psnr(c, s):.4f}, ssim: {ssim(c, s):.4f}")

# ---------------------------------------------------------
# RECOVER: extracts secret from a stego image only
# ---------------------------------------------------------
def recover(stego_path, model_path, out_path):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = StegoAutoencoder(device=device)
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.eval()

    stego = load_image(stego_path).to(device)

    with torch.no_grad():
        # We pass cover=stego because model requires two args, but ignores secret internally
        _, recovered = model(stego, stego)

    save_image(recovered, out_path)
    return out_path

# ---------------------------------------------------------
# CLI
# ---------------------------------------------------------
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd")

    h = sub.add_parser("hide")
    h.add_argument("--cover", type=str)
    h.add_argument("--secret", type=str)
    h.add_argument("--out", type=str)
    h.add_argument("--model", type=str)

    r = sub.add_parser("recover")
    r.add_argument("--stego", type=str)
    r.add_argument("--out", type=str)
    r.add_argument("--model", type=str)

    args = parser.parse_args()

    if args.cmd == "hide":
        hide(args.cover, args.secret, args.out, args.model)

    elif args.cmd == "recover":
        recover(args.stego, args.model, args.out)
