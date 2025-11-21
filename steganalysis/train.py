import os
import torch
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from PIL import Image
import glob
from steganalysis.model import StegAnalysisCNN

class StegoDataset(Dataset):
    def __init__(self, clean_dir, stego_dir):
        self.clean = sorted(glob.glob(os.path.join(clean_dir, "*")))
        self.stego = sorted(glob.glob(os.path.join(stego_dir, "*")))
        self.files = [(f, 0) for f in self.clean] + [(f, 1) for f in self.stego]

        self.transform = transforms.Compose([
            transforms.Resize((128, 128)),
            transforms.ToTensor()
        ])

    def __len__(self):
        return len(self.files)

    def __getitem__(self, idx):
        path, label = self.files[idx]
        img = Image.open(path).convert("RGB")
        img = self.transform(img)
        return img, torch.tensor(label, dtype=torch.long)

def train(model, loader, optim, device, epochs):
    loss_fn = torch.nn.CrossEntropyLoss()
    for e in range(epochs):
        total = 0
        correct = 0
        total_loss = 0
        for x, y in loader:
            x = x.to(device)
            y = y.to(device)
            out = model(x)
            loss = loss_fn(out, y)

            optim.zero_grad()
            loss.backward()
            optim.step()

            total += y.size(0)
            correct += (out.argmax(1) == y).sum().item()
            total_loss += loss.item()

        acc = correct / total
        print(f"epoch {e+1}/{epochs} loss: {total_loss/len(loader):.4f} acc: {acc:.4f}")

if __name__ == "__main__":
    clean = "data/detector/clean"
    stego = "data/detector/stego"
    device = "cuda" if torch.cuda.is_available() else "cpu"

    dataset = StegoDataset(clean, stego)
    loader = DataLoader(dataset, batch_size=16, shuffle=True)

    model = StegAnalysisCNN().to(device)
    optim = torch.optim.Adam(model.parameters(), lr=1e-3)

    train(model, loader, optim, device, epochs=10)

    os.makedirs("models", exist_ok=True)
    torch.save(model.state_dict(), "models/steganalysis_cnn.pth")
    print("saved steganalysis model")
