# KrishiDoc Dataset

## Structure
```
dataset/
├── healthy/
│   ├── wheat_healthy/        → place healthy wheat images here
│   ├── rice_healthy/         → place healthy rice images here
│   ├── cotton_healthy/       → place healthy cotton images here
│   └── soybean_healthy/      → place healthy soybean images here
│
└── diseases/
    ├── wheat_rust/           → place wheat rust images here
    ├── wheat_blight/         → place wheat blight images here
    ├── rice_blast/           → place rice blast images here
    ├── rice_brownspot/       → place rice brown spot images here
    ├── cotton_leafspot/      → place cotton leaf spot images here
    ├── cotton_blight/        → place cotton blight images here
    ├── soybean_rust/         → place soybean rust images here
    └── soybean_mosaic/       → place soybean mosaic images here
```

## How to add images
1. Download PlantVillage dataset from:
   https://www.kaggle.com/datasets/emmarex/plantdisease
2. Place images in the correct folder above
3. Each folder = one disease class
4. Minimum 100 images per class recommended

## Dataset Info
- Source: PlantVillage Dataset
- Total classes: 38 disease types
- Total images: 54,306
- Format: JPG/PNG

## Future Training
Once enough images are collected, run:
```
python backend/train.py
```
This will train KrishiDoc-CNN-v1.0 on your dataset.

## Current Status
- Model: KrishiDoc-CNN-v1.0 (mock, ready for training)
- Dataset: PlantVillage (reference)
- Real diagnosis: Powered by Google Gemini AI
