# CycleGAN-VAE for CT to MRI Image Translation

## 📌 Project Overview
This project implements an **image-to-image translation model** using **CycleGAN with a Variational Autoencoder (VAE) bottleneck**. The goal is to convert **CT scans** into **MRI images** and vice versa using **unpaired medical imaging data**.

## 🚀 Architecture Details
This model consists of:
- **Generators**: Two networks for CT → MRI and MRI → CT translation.
- **Discriminators**: Two discriminators to distinguish real vs. fake images.
- **Cycle Consistency Loss**: Ensures that translating from CT → MRI → CT retains the original content.
- **VAE Bottleneck**: Regularizes the latent space to improve stability.

### 📌 Model Flow
```
          +-------------------+       +-------------------+
          |  Generator G_A→B  |       |  Generator G_B→A  |
          |  (CT → MRI)       |       |  (MRI → CT)       |
          +-------------------+       +-------------------+
                  |                           |
                  |                           |
                  v                           v
          +-------------------+       +-------------------+
          |  Fake MRI (B_fake)|       |  Fake CT (A_fake) |
          +-------------------+       +-------------------+
                  |                           |
                  |                           |
                  v                           v
          +-------------------+       +-------------------+
          |  Discriminator D_B|       |  Discriminator D_A|
          |  (MRI Domain)    |       |  (CT Domain)      |
          +-------------------+       +-------------------+
                  |                           |
                  |                           |
                  v                           v
          +-------------------+       +-------------------+
          |  Real/Fake MRI    |       |  Real/Fake CT     |
          |  Classification   |       |  Classification   |
          +-------------------+       +-------------------+

          +-------------------+       +-------------------+
          |  Cycle Consistency|       |  Cycle Consistency|
          |  MRI → CT → MRI   |       |  CT → MRI → CT    |
          +-------------------+       +-------------------+
```

## 📦 Installation
Clone the repository and install dependencies:
```sh
git clone https://github.com/your-repo/cyclegan-vae.git
cd cyclegan-vae
pip install -r requirements.txt
```

## 📊 Dataset Preparation
- Prepare **unpaired CT and MRI images** in separate folders.
- Example dataset structure:
```
/dataset
   ├── trainA  (CT images)
   ├── trainB  (MRI images)
   ├── testA   (CT test images)
   ├── testB   (MRI test images)
```
##Project directory 
project/
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── main.js
│   ├── images/
│   │   ├── samples/
│   │   └── results/
│   └── uploads/
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── try_now.html
│   ├── result.html
│   ├── samples.html
│   └── model_info.html
└── app.py
└── code.ipynb

Gvie app.py and remove if any errro will be there
## 🔥 Training the Model
Run the training script:

run code.ipynb: keep saved models files in models folder


## 🖼️ Test the Model
Run the inference script on new images:
```sh
python app.py
```

## ⚙️ Loss Functions Used
- **Adversarial Loss**: Ensures that generated images are realistic.
- **Cycle Consistency Loss**: Maintains structural consistency.
- **KL Divergence Loss**: Regularizes the latent space.

