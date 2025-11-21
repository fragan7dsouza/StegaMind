import numpy as np
from skimage.metrics import structural_similarity as ssim_sk

def psnr(a, b):
    a = np.array(a).astype(np.float32)
    b = np.array(b).astype(np.float32)
    mse = np.mean((a - b) ** 2)
    if mse == 0:
        return 100
    return 20 * np.log10(255.0 / np.sqrt(mse))

def ssim(a, b):
    a = np.array(a).astype(np.uint8)
    b = np.array(b).astype(np.uint8)
    return ssim_sk(a, b, channel_axis=2)
