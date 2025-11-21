import os
import torch
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms
from PIL import Image
import glob

class ImagePairDataset(Dataset):
    def __init__(self, cover_folder, secret_folder):
        self.covers = sorted(glob.glob(os.path.join(cover_folder, "*")))
        self.secrets = sorted(glob.glob(os.path.join(secret_folder, "*")))
        self.t = transforms.Compose([
            transforms.Resize((128, 128)),
            transforms.ToTensor()
        ])

    def __len__(self):
        return min(len(self.covers), len(self.secrets))

    def __getitem__(self, idx):
        c = Image.open(self.covers[idx]).convert("RGB")
        s = Image.open(self.secrets[idx]).convert("RGB")
        return self.t(c), self.t(s)

def train_loop(model, dataloader, optim, device, epochs):
    mse = torch.nn.MSELoss()
    for e in range(epochs):
        model.train()
        total = 0
        for cover, secret in dataloader:
            cover, secret = cover.to(device), secret.to(device)
            stego, rec = model(cover, secret)
            lc = mse(stego, cover)
            ls = mse(rec, secret)
            loss = lc + 2 * ls
            optim.zero_grad()
            loss.backward()
            optim.step()
            total += loss.item()
        print(f"epoch {e+1}/{epochs}, loss: {total/len(dataloader):.6f}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--cover_folder", type=str, default="data/cover_images")
    parser.add_argument("--secret_folder", type=str, default="data/secrets")
    parser.add_argument("--epochs", type=int, default=5)
    parser.add_argument("--batch", type=int, default=8)
    args = parser.parse_args()

    device = "cuda" if torch.cuda.is_available() else "cpu"

    from steganography.model import StegoAutoencoder
    model = StegoAutoencoder(device=device)

    optim = torch.optim.Adam(
        list(model.encoder.parameters()) +
        list(model.decoder.parameters()),
        lr=1e-3
    )

    dataset = ImagePairDataset(args.cover_folder, args.secret_folder)
    dataloader = DataLoader(dataset, batch_size=args.batch, shuffle=True, num_workers=0)

    train_loop(model, dataloader, optim, device, args.epochs)

    os.makedirs("models", exist_ok=True)
    torch.save(model.state_dict(), "models/stego_autoencoder.pth")
    print("model saved to models/stego_autoencoder.pth")
