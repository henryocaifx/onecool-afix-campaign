#!/usr/bin/env python3
"""Typeset original campaign graphics and synthesize an original sonic signature.

The real application capture is composited only during the FFmpeg edit. This
script does not synthesize or alter application controls or generated art.
"""
from pathlib import Path
import json
import math
import wave
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "graphics"
OUT.mkdir(exist_ok=True)
W, H = 2520, 1080
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(size, bold=False):
    return ImageFont.truetype(BOLD if bold else REG, size)


def center(draw, y, value, size, color, bold=False):
    f = font(size, bold)
    box = draw.textbbox((0, 0), value, font=f)
    draw.text(((W - box[2]) / 2, y), value, font=f, fill=color)


def gradient_text(im, xy, value, size, bold=True):
    mask = Image.new("L", (W, H))
    ImageDraw.Draw(mask).text(xy, value, font=font(size, bold), fill=255)
    colors = np.array([[238, 69, 173], [128, 88, 239], [16, 185, 218]], dtype=float)
    xmin = int(xy[0])
    width = int(ImageDraw.Draw(mask).textlength(value, font=font(size, bold)))
    strip = np.zeros((H, W, 3), dtype=np.uint8)
    for x in range(W):
        t = np.clip((x - xmin) / max(1, width), 0, 1) * 2
        j = min(int(t), 1)
        strip[:, x] = colors[j] * (1 - (t-j)) + colors[j+1] * (t-j)
    im.paste(Image.fromarray(strip), (0, 0), mask)


films = json.loads((ROOT / "records" / "films.json").read_text())
for i, film in enumerate(films):
    # Restrained dark graphic field; the story footage provides the spectacle.
    yy, xx = np.mgrid[0:H, 0:W]
    field = np.zeros((H, W, 3), dtype=float) + np.array([7, 8, 14])
    for cx, cy, col in [(780, 470, [20, 5, 35]), (1700, 490, [0, 18, 30])]:
        g = np.exp(-(((xx-cx)/650)**2 + ((yy-cy)/480)**2))
        field += g[..., None] * np.array(col)
    im = Image.fromarray(np.uint8(np.clip(field, 0, 255)))
    d = ImageDraw.Draw(im)
    d.line((155, 125, W-155, 125), fill=(45, 44, 62), width=2)
    d.text((160, 153), "AIFX STUDIO  /  ORIGINAL WORLDS", font=font(24), fill=(154, 154, 174))
    d.text((W-345, 153), f"FILM {i+1:02}", font=font(24), fill=(154, 154, 174))
    brand_font = font(162, True)
    first = "AIFX "
    fw = d.textlength(first, font=brand_font)
    sw = d.textlength("Studio", font=brand_font)
    bx = (W-fw-sw)/2
    d.text((bx, 290), first, font=brand_font, fill=(250, 250, 253))
    gradient_text(im, (bx+fw, 290), "Studio", 162)
    d = ImageDraw.Draw(im)
    center(d, 510, "AI-powered filmmaking", 34, (163, 161, 185))
    center(d, 610, film["line"], 55, (248, 247, 252))
    center(d, 794, "charsiufan.onecool.ai", 48, (218, 221, 238), True)
    d.line((W//2-105, 754, W//2+105, 754), fill=(142, 86, 239), width=4)
    d.line((155, 946, W-155, 946), fill=(45, 44, 62), width=2)
    im.save(OUT / f"{film['id']}-end.png")

    # Small opening product identifier, no unverified feature claims.
    bug = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bd = ImageDraw.Draw(bug)
    bd.rounded_rectangle((W-620, 60, W-60, 181), radius=24, fill=(8, 9, 17, 225), outline=(99, 72, 143, 180), width=2)
    bd.text((W-580, 78), "AIFX Studio", font=font(39, True), fill=(255, 255, 255, 255))
    bd.text((W-580, 133), "Make room for imagination.", font=font(23), fill=(198, 192, 218, 255))
    bug.save(OUT / f"{film['id']}-bug.png")

    # Editorial product strip. A real public-page crop will sit in the left box.
    panel = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    pd = ImageDraw.Draw(panel)
    pd.rounded_rectangle((72, 710, W-72, H-52), radius=26, fill=(7, 8, 16, 242), outline=(113, 81, 169, 200), width=2)
    pd.text((810, 744), "AIFX Studio", font=font(55, True), fill=(250, 249, 255))
    pd.text((810, 829), film["line"], font=font(41), fill=(226, 221, 243))
    pd.text((810, 924), "charsiufan.onecool.ai", font=font(32), fill=(160, 159, 190))
    pd.text((149, 986), "AI-POWERED FILMMAKING", font=font(16), fill=(137, 135, 161))
    panel.save(OUT / f"{film['id']}-product.png")

    # Trailer title graphics remain separate from the source footage.
    if i >= 2:
        title = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        td = ImageDraw.Draw(title)
        td.rounded_rectangle((290, 265, W-290, 565), radius=18, fill=(4, 5, 12, 200))
        center(td, 300, film["title"].upper(), 104 if i == 2 else 83, (248, 246, 255, 255), True)
        center(td, 465, "AN AIFX STUDIO ORIGINAL WORLD", 25, (190, 178, 218, 255))
        title.save(OUT / f"{film['id']}-title.png")

    # Original three-note campaign motif. No samples or existing compositions.
    sr = 48000
    t = np.arange(4*sr) / sr
    audio = np.zeros((len(t), 2))
    base_freqs = [293.6648, 440.0, 587.3295]
    for n, f in enumerate(base_freqs):
        start = .08 + .34*n
        u = t-start
        env = np.where(u >= 0, (1-np.exp(-np.maximum(u,0)*95))*np.exp(-np.maximum(u,0)*1.75), 0)
        tone = np.sin(2*math.pi*f*u) + .22*np.sin(2*math.pi*2*f*u) + .08*np.sin(2*math.pi*3.001*f*u)
        gain = .11 if i < 2 else .14
        pan = [.35, .65] if n % 2 else [.65, .35]
        audio += gain*(tone*env)[:,None]*np.array(pan)[None,:]
    fade = np.minimum(1, np.maximum(0, (4-t)/.5))
    audio *= fade[:,None]
    pcm = np.int16(np.clip(audio, -1, 1)*32767)
    with wave.open(str(OUT / f"{film['id']}-signature.wav"), "wb") as wav:
        wav.setnchannels(2); wav.setsampwidth(2); wav.setframerate(sr); wav.writeframes(pcm.tobytes())
print("Created four end cards, product graphics, two trailer titles, and four original stereo signatures.")
