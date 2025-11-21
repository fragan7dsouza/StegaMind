import os
import torch
from PIL import Image
import torchvision.transforms as T
from steganography.model import StegoAutoencoder

t = T.Compose([
    T.Resize((128,128)),
    T.ToTensor()
])

def load_img(path):
    return t(Image.open(path).convert("RGB")).unsqueeze(0)

def save_img(tensor, path):
    arr = (tensor.squeeze().permute(1,2,0).detach().cpu().numpy()*255).clip(0,255).astype("uint8")
    Image.fromarray(arr).save(path)

def main():
    cover_dir = "data/cover_images"
    secret_dir = "data/secrets"
    out_dir = "data/detector/stego"
    model_path = "models/stego_autoencoder.pth"

    os.makedirs(out_dir, exist_ok=True)

    model = StegoAutoencoder(device="cpu")
    model.load_state_dict(torch.load(model_path, map_location="cpu"))
    model.eval()

    covers = sorted(os.listdir(cover_dir))
    secrets = sorted(os.listdir(secret_dir))

    count = 0
    for c, s in zip(covers, secrets):
        cover = load_img(os.path.join(cover_dir, c))
        secret = load_img(os.path.join(secret_dir, s))

        with torch.no_grad():
            stego, _ = model(cover, secret)

        out = os.path.join(out_dir, f"stego_{count}.png")
        save_img(stego, out)
        count += 1

        if count >= 2000:
            break

    print("Generated", count, "stego images.")

if __name__ == "__main__":
    main()
