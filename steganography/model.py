import torch
import torch.nn as nn
import torch.nn.functional as F

def conv_block(in_ch, out_ch):
    return nn.Sequential(
        nn.Conv2d(in_ch, out_ch, 3, padding=1),
        nn.BatchNorm2d(out_ch),
        nn.ReLU(inplace=True),
        nn.Conv2d(out_ch, out_ch, 3, padding=1),
        nn.BatchNorm2d(out_ch),
        nn.ReLU(inplace=True)
    )

def up_conv(in_ch, out_ch):
    return nn.Sequential(
        nn.Upsample(scale_factor=2, mode='bilinear', align_corners=False),
        nn.Conv2d(in_ch, out_ch, 3, padding=1),
        nn.BatchNorm2d(out_ch),
        nn.ReLU(inplace=True)
    )

class UNet(nn.Module):
    def __init__(self, in_ch=3, base=32):
        super().__init__()
        self.enc1 = conv_block(in_ch, base)
        self.enc2 = conv_block(base, base * 2)
        self.enc3 = conv_block(base * 2, base * 4)
        self.pool = nn.MaxPool2d(2)
        self.bottleneck = conv_block(base * 4, base * 8)
        self.up3 = up_conv(base * 8, base * 4)
        self.dec3 = conv_block(base * 8, base * 4)
        self.up2 = up_conv(base * 4, base * 2)
        self.dec2 = conv_block(base * 4, base * 2)
        self.up1 = up_conv(base * 2, base)
        self.dec1 = conv_block(base * 2, base)
        self.final = nn.Conv2d(base, 3, 1)

    def forward(self, x):
        c1 = self.enc1(x)
        p1 = self.pool(c1)
        c2 = self.enc2(p1)
        p2 = self.pool(c2)
        c3 = self.enc3(p2)
        p3 = self.pool(c3)
        bn = self.bottleneck(p3)
        u3 = self.up3(bn)
        d3 = self.dec3(torch.cat([c3, u3], dim=1))
        u2 = self.up2(d3)
        d2 = self.dec2(torch.cat([c2, u2], dim=1))
        u1 = self.up1(d2)
        d1 = self.dec1(torch.cat([c1, u1], dim=1))
        return self.final(d1)

class StegoAutoencoder(nn.Module):
    def __init__(self, device='cpu'):
        super().__init__()
        self.encoder = UNet(in_ch=6)
        self.decoder = UNet(in_ch=3)
        self.to(device)

    def forward(self, cover, secret):
        x = torch.cat([cover, secret], dim=1)
        stego = self.encoder(x)
        rec = self.decoder(stego)
        return stego, rec
