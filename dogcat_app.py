"""Dog vs Cat comparison app.

Pick a photo and the app shows how "dog-like" and how "cat-like" it is.
It uses MobileNetV2, a small AI model already trained on ImageNet
(which includes ~118 dog breed classes and 5 domestic cat classes).
"""
import tkinter as tk
from tkinter import filedialog, ttk

import torch
from PIL import Image, ImageTk
from torchvision import models

# ---- 1. Load the pretrained model (downloads ~14 MB the first time) ----
weights = models.MobileNet_V2_Weights.DEFAULT
model = models.mobilenet_v2(weights=weights)
model.eval()                      # evaluation mode: we are predicting, not training
preprocess = weights.transforms() # resizes/normalises images the way the model expects


# ---- 2. The AI part: turn an image file into dog and cat scores ----
def classify(path):
    image = Image.open(path).convert("RGB")
    batch = preprocess(image).unsqueeze(0)          # add a "batch of 1" dimension
    with torch.no_grad():                           # no learning, so no gradients needed
        probs = torch.softmax(model(batch)[0], dim=0)  # 1000 probabilities that sum to 1
    dog = probs[151:269].sum().item()               # ImageNet classes 151-268 are dogs
    cat = probs[281:286].sum().item()               # ImageNet classes 281-285 are cats
    return image, dog, cat


# ---- 3. The window ----
root = tk.Tk()
root.title("Dog vs Cat")
root.geometry("420x560")

photo_label = tk.Label(root, text="No image yet", width=40, height=15, relief="groove")
photo_label.pack(pady=10)

verdict = tk.Label(root, text="", font=("Segoe UI", 16, "bold"))
verdict.pack(pady=5)

dog_text = tk.Label(root, text="Dog: -")
dog_text.pack()
dog_bar = ttk.Progressbar(root, length=300, maximum=100)
dog_bar.pack(pady=2)

cat_text = tk.Label(root, text="Cat: -")
cat_text.pack()
cat_bar = ttk.Progressbar(root, length=300, maximum=100)
cat_bar.pack(pady=2)


def choose_image():
    path = filedialog.askopenfilename(
        filetypes=[("Images", "*.jpg *.jpeg *.png *.bmp *.webp")]
    )
    if not path:
        return  # user pressed Cancel

    image, dog, cat = classify(path)

    # show the picture
    preview = image.copy()
    preview.thumbnail((300, 300))
    tk_image = ImageTk.PhotoImage(preview)
    photo_label.configure(image=tk_image, text="", width=300, height=300)
    photo_label.image = tk_image  # keep a reference or Tkinter drops the picture

    # compare dog and cat
    total = dog + cat
    if total < 0.10:
        verdict.configure(text="Neither a dog nor a cat?")
        dog_text.configure(text="Dog: -")
        cat_text.configure(text="Cat: -")
        dog_bar["value"] = 0
        cat_bar["value"] = 0
        return

    dog_pct = dog / total * 100
    cat_pct = cat / total * 100
    verdict.configure(text="It's a DOG!" if dog_pct > cat_pct else "It's a CAT!")
    dog_text.configure(text=f"Dog: {dog_pct:.1f}%")
    cat_text.configure(text=f"Cat: {cat_pct:.1f}%")
    dog_bar["value"] = dog_pct
    cat_bar["value"] = cat_pct


tk.Button(root, text="Choose image...", command=choose_image, padx=10, pady=5).pack(pady=15)

root.mainloop()
