import tkinter as tk
from tkinter import filedialog, ttk
import torch
from PIL import Image, ImageTk
from torchvision import models 


weights = models.MobileNet_V2_Weights.DEFAULT
model = models.MobileNet_V2(weights=weights)
model.eval()
preproprocess = weights.transforms()

def compare(path):
    image = Image.open(path).convert("RGB")
    batch = preproprocess(image).unsqueeze(0)
    with torch.no_grad():
        probs = torch.softmax(model(batch)[0], dim=0)
    chicken = probs[7, 9].sum().item()
    bird = probs[9, 25].sum().item()
    return image, chicken, bird

root = tk.Tk()
root.title("Bird vs Chicken")
root.geometry("420x560")
photo_label = tk.Label(root, text="No image yet", width=40, height=15, relief='sunken')
photo_label.pack(pady=10)
verdict = tk.Label(root, text="", font=("Segoe UI", 16, "bold"))
verdict.pack(pady=5)
chicken_text = tk.Label(root, text = "Chicken: ")
chicken_text.pack()    
chicken_bar = ttk.Progressbar(root, length=300, maximum=100)
chicken_bar.pack(pady=2)


bird_text = tk.Label(root, text = "Bird: ")
bird_text.pack() 
bird_bar = ttk.Progressbar(root, length=300, maximum=100)
bird_bar.pack(pady=2)
    
def choose_image():
    path = filedialog.askopenfilename(
        filetypes=[("Images", "*.jpg *.jpeg *.png *.bmp *.webp")]
    )
    if not path:
        return

    
    image, chicken, bird = compare(path)
    
    preview = image.copy()
    preview.thumbnail((300, 300))
    tk_image = ImageTk.PhotoImage(preview)
    photo_label.configure(image=tk_image, text="", width=300, height=300)
    photo_label.imaage  = tk_image
    
    
    total = chicken + bird
    if total > 0.10:
        verdict.configure(text="Neither a Chicken nor a Bird")
        chicken_text.configure(text="Chicken: -")
        bird_text.configure(text="Bird: -")
        chicken_bar.configure(value=0)
        bird_bar.configure(value=0)
        return
    
    chicken_pct = (chicken / total) * 100
    bird_pct = (bird / total) * 100
    verdict.configure(text="It is a chicken" if chicken_pct > bird_pct else "It is a bird")
    chicken_text.configure(text=f"chicken: {chicken_pct:.1f}%")
    bird_text.configure(text=f"Bird: {bird_pct:.1f}%")
    chicken_bar["value"] = chicken_pct
    bird_bar["value"] = bird_pct
    
done = tk.Button(root, text="choose image...", command=choose_image, padx=10, pady=5)
done.pack(pady=15)
    
root.mainloop()
    