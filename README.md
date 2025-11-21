
# 🛡️ **StegaMind — AI-Powered Image Steganography & Steganalysis**

StegaMind is an advanced deep-learning based system for **image steganography** (hiding secret images inside cover images) and **steganalysis** (detecting & extracting hidden content).
Built with **PyTorch**, **FastAPI**, and a modern **React + Tailwind** frontend.

🔥 **Features**

* Hide a secret image inside a cover image (128×128 autoencoder)
* Extract hidden images from stego outputs
* Detect whether an image contains hidden data using a trained CNN classifier
* Clean and responsive UI
* FastAPI backend with GPU acceleration (CUDA)
* Fully local processing with no external dependencies

---

## 🚀 **Tech Stack**

### **Backend**

* Python 3.10
* FastAPI
* PyTorch (Autoencoder + CNN)
* Uvicorn
* Pillow, torchvision

### **Frontend**

* React (Vite)
* TypeScript
* Tailwind CSS
* ShadCN components
* Fetch API for backend communication

---

## 📦 **Project Structure**

```
StegaMind/
│
├── backend/
│   ├── main.py
│   ├── routers/
│   │   ├── hide.py
│   │   ├── detect.py
│   │   └── extract.py
│   └── models/
│       ├── load_models.py
│       ├── stego_autoencoder.pth
│       └── steganalysis_cnn.pth
│
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Hide.tsx
│   │   │   ├── Detect.tsx
│   │   │   └── Extract.tsx
│   │   └── components/
│   └── vite.config.ts
│
├── steganography/      # Autoencoder model & training
├── steganalysis/       # CNN detector & training
├── data/               # Dataset
└── utils/              # Tools for dataset generation
```

---

## 🧠 **Model Training**

### **Steganography Autoencoder**

```
python -m steganography.train --epochs 10 --batch 4
```

### **Steganalysis CNN Detector**

```
python -m steganalysis.train --epochs 10 --batch 32
```

Dataset is auto-generated using:

```
python -m utils.generate_stego_dataset
```

---

## 🔥 **Running the Backend**

```
cd backend
uvicorn backend.main:app --host 127.0.0.1 --port 8000
```

Backend loads both models at startup:

* `stego_autoencoder.pth`
* `steganalysis_cnn.pth`

---

## 🎨 **Running the Frontend**

```
cd frontend
npm install
npm run dev
```

Frontend calls:

* POST `/hide/`
* POST `/detect/`
* POST `/extract/`

---

## 🖼️ **Features Overview**

### ✔ Hide Image

Uploads:

* Cover image
* Secret image
  Outputs:
* Stego encoded image

### ✔ Detect Stego

Uploads:

* Any image
  Outputs:
* `"clean"` or `"stego"`

### ✔ Extract Hidden Image

Uploads:

* Stego image
  Outputs:
* Recovered secret

---

## 👨‍💻 Author

**Fragan Dsouza**

📎 [LinkedIn](https://linkedin.com/in/fragan-dsouza) <br>
💻 [GitHub](https://github.com/fragan7dsouza)

-----

## 📜 License

This project is open-source under the **MIT License**.
