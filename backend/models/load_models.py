import torch
from steganography.model import StegoAutoencoder
from steganalysis.model import StegAnalysisCNN

# SINGLE source of truth
MODELS = {
    "stego": None,
    "detect": None
}

def load_all():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print("==== MODEL LOADING START ====")
    print("Device:", device)

    # Load StegoAutoencoder
    try:
        print("Loading StegoAutoencoder...")
        stego = StegoAutoencoder(device=device)
        stego.load_state_dict(torch.load("models/stego_autoencoder.pth", map_location=device))
        stego.to(device)
        stego.eval()
        MODELS["stego"] = stego
        print("✔ Stego model loaded")
    except Exception as e:
        print("❌ Stego model FAILED:", e)

    # Load StegAnalysisCNN
    try:
        print("Loading StegAnalysisCNN...")
        detect = StegAnalysisCNN()
        detect.load_state_dict(torch.load("models/steganalysis_cnn.pth", map_location=device))
        detect.to(device)
        detect.eval()
        MODELS["detect"] = detect
        print("✔ Detect model loaded")
    except Exception as e:
        print("❌ Detect model FAILED:", e)

    print("==== MODEL LOADING END ====")
