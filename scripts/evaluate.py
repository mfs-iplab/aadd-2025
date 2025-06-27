"""
Overview

This script evaluates the robustness of one or more image-classification
models against *adversarial versions* of a given image set.  
For every original / adversarial image pair it:

1. **Computes similarity** (mean RGB SSIM).
2. **Runs each classifier** on the adversarial image.
3. **Flags successful attacks** (prediction == “real” class).
4. **Aggregates** SSIM-weighted attack indicators into a final score.

At the end it prints a detailed per-model breakdown and, if requested,
saves a JSON report.

How it Works

* **Configuration** – All runtime options are provided via a YAML file  
  (`--config <path>`). Key fields:  
  `models_dir`, `classifiers`, `original_root`, `adv_root`, `device`,
  `dct_log_scale`, `aggregate`, `save_json`.

Dependencies

* Python ≥ 3.9
* PyTorch ≥ 2.1  (`torch`, `torchvision`)
* NumPy, SciPy, scikit-image, Pillow
* PyYAML, tqdm

GPU acceleration is automatic if CUDA is available and `device: auto`
in the YAML; otherwise CPU is used.

Quick Use

```bash
# 1. Install requirements (example with pip)
pip install torch torchvision pyyaml numpy pillow scikit-image scipy tqdm

# 2. Prepare only these directories in the config:
#    • models_dir/         →  *.pth weight files (names match 'classifiers')
#    • original_root/      →  clean PNG images
#    • adv_root/           →  adversarial PNG counterparts (same structure)

# 3. Run evaluation
python evaluate.py --config config.yaml
"""


import argparse, warnings, json
from pathlib import Path
from glob import glob

import yaml               # PyYAML
import numpy as np
from PIL import Image
from skimage.metrics import structural_similarity as ssim

import torch
import torch.nn as nn
import torchvision.transforms as T
from torchvision.models import resnet50, densenet121, vit_b_16
from torchvision import models as tv_models
from tqdm import tqdm
from scipy.fftpack import dct  # per DCT 2‑D

CLASS_IDX_REAL = 0
DEVICE_DEFAULT = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
IMAGE_EXTS = {'.png', '.jpg', '.jpeg', '.bmp', '.tiff'}

CLASSES = 2

def create_resnet18_dct():
    model = tv_models.resnet18(pretrained=False)
    model.conv1 = nn.Conv2d(1, 64, kernel_size=7, stride=2, padding=3, bias=False)
    model.fc = nn.Sequential(
        nn.Dropout(0.2),
        nn.Linear(model.fc.in_features, CLASSES)
    )
    return model

def create_densenet121_dct():
    model = tv_models.densenet121(pretrained=False)
    model.features.conv0 = nn.Conv2d(1, 64, kernel_size=7, stride=2, padding=3, bias=False)
    model.classifier = nn.Sequential(
        nn.Dropout(0.2),
        nn.Linear(model.classifier.in_features, CLASSES)
    )
    return model

def load_cfg(cfg_path: str) -> dict:
    with open(cfg_path, 'r') as f:
        cfg = yaml.safe_load(f)
    print(f"[CONFIG] Loaded configuration from {cfg_path}")
    return cfg


def get_device(choice: str):
    if choice == 'auto':
        print(f"[DEVICE] Using device {DEVICE_DEFAULT}")
        return DEVICE_DEFAULT
    print("[DEVICE] Using CPU")
    return torch.device('cpu')


def pil_to_np_rgb(path):
    return np.array(Image.open(path).convert("RGB"))


def compute_ssim_rgb(im1, im2):
    # media SSIM sui 3 canali
    return sum(
        ssim(im1[..., c], im2[..., c], data_range=255)
        for c in range(3)
    ) / 3.0

def dct2(np_img):
    return dct(dct(np_img, axis=0, norm='ortho'), axis=1, norm='ortho')


def build_dct_transform(log_scale: bool):
    def _transform(pil_img: Image.Image):
        # step 1: grayscale
        img = pil_img.convert('L')
        # step 2: resize to 256×256 max side
        if max(img.size) > 256:
            img = img.resize((256, 256), Image.Resampling.LANCZOS)
        # step 3: central crop 128×128
        w, h = img.size
        left = (w - 128) // 2
        top = (h - 128) // 2
        img = img.crop((left, top, left + 128, top + 128))
        # step 4: DCT
        np_img = np.array(img, dtype=np.float32)
        dct_img = dct2(np_img)
        if log_scale:
            dct_img = np.log(np.abs(dct_img) + 1e-6)
        tensor = torch.from_numpy(dct_img).unsqueeze(0)  # 1×128×128
        return tensor
    return _transform

def build_spatial_transform(model_name):
    if model_name == 'vit_b_16':
        return T.Compose([
            T.Resize((256, 256)),
            T.CenterCrop((224, 224)),
            T.ToTensor(),
            T.Normalize(mean=[0.485, 0.456, 0.406],
                        std=[0.229, 0.224, 0.225])
        ])
    return T.Compose([
        T.Resize((256, 256)),
        T.ToTensor(),
        T.Normalize(mean=[0.485, 0.456, 0.406],
                    std=[0.229, 0.224, 0.225])
    ])

def load_model(name, weight_path, device):
    print(f"[MODEL] Loading '{name}' weights from {weight_path}...")
    if name == 'resnet50':
        model = resnet50()
        model.fc = nn.Linear(model.fc.in_features, CLASSES)
    elif name == 'densenet121':
        model = densenet121()
        model.classifier = nn.Linear(model.classifier.in_features, CLASSES)
    elif name == 'vit_b_16':
        model = vit_b_16()
        model.heads.head = nn.Linear(model.heads.head.in_features, CLASSES)
    elif name == 'resnet18_dct':
        model = create_resnet18_dct()
    elif name == 'densenet121_dct':
        model = create_densenet121_dct()
    else:
        raise ValueError(f"Unsupported model '{name}'")

    state = torch.load(weight_path, map_location=device)
    model.load_state_dict(state)
    model.eval().to(device)
    print(f"[MODEL] '{name}' ready on {device}\n")
    return model

def evaluate(cfg):
    device = get_device(cfg.get('device', 'auto'))

    log_scale = bool(cfg.get('dct_log_scale', False))

    # --- load classifiers
    models_dir = Path(cfg['models_dir'])
    clf_names = cfg['classifiers']
    classifiers = {}
    for name in clf_names:
        w_path = models_dir / f"{name}.pth"
        if not w_path.exists():
            raise FileNotFoundError(f"Weight file for '{name}' not found: {w_path}")

        if name.endswith('_dct'):
            transform = build_dct_transform(log_scale)
        else:
            transform = build_spatial_transform(name)

        classifiers[name] = {
            'model': load_model(name, w_path, device),
            'transform': transform,
            'indicators': [],
            'ssim_vals': []
        }
    num_classifiers = len(classifiers)
    print(f"[SETUP] {num_classifiers} classifiers loaded\n")

    # dataset paths
    original_root = Path(cfg['original_root'])
    adv_root      = Path(cfg['adv_root'])

    # orig_paths = glob(str(original_root / "**/*.png"), recursive=True)

    orig_paths = [p for p in original_root.rglob("*")
                if p.is_file() and p.suffix.lower() in IMAGE_EXTS]
    if not orig_paths:
        raise RuntimeError("No PNG images found under original_root.")
    print(f"[DATA] {len(orig_paths)} original images detected\n")

    running_sum = 0.0
    total_pairs = 0

    for o_path in tqdm(orig_paths, desc="Images"):
        rel = Path(o_path).relative_to(original_root)
        # 2) provo adv con stessa estensione
        a_path = adv_root / rel
        if not a_path.exists():
            # altrimenti cerco qualunque file con lo stesso stem
            parent = adv_root / rel.parent
            stem = rel.stem
            matches = list(parent.glob(f"{stem}.*"))
            if matches:
                a_path = matches[0]
            else:
                warnings.warn(f"Missing adversarial counterpart for {rel}")
                continue

        print(f"[IMAGE] {rel}")

        # 3) compute SSIM con try/except sulle dimensioni
        img_o = pil_to_np_rgb(o_path)
        img_a = pil_to_np_rgb(a_path)
        try:
            ssim_val = compute_ssim_rgb(img_o, img_a)
        except Exception as e:
            warnings.warn(f"SSIM failed for {rel}: {e}")
            ssim_val = 0.0

        print(f"    SSIM: {ssim_val:.4f}")

        pair_contribution = 0.0

        for name, pack in classifiers.items():
            tensor = pack['transform'](Image.fromarray(img_a))
            tensor = tensor.unsqueeze(0).to(device)
            with torch.no_grad():
                pred = pack['model'](tensor).argmax(1).item()
            indicator = int(pred == CLASS_IDX_REAL)

            print(f"    [MODEL] {name:<15} → pred={'real' if pred==0 else 'fake'}({pred})  indicator={indicator}")

            pack['indicators'].append(indicator)
            pack['ssim_vals'].append(ssim_val)
            pair_contribution += ssim_val * indicator

        print(f"    Contribution to score: {pair_contribution:.4f}")

        running_sum += pair_contribution
        total_pairs += 1

    if total_pairs == 0:
        print("[RESULT] No valid image pairs found – score = 0")
        return

    if cfg.get('aggregate', 'mean').lower() == 'mean':
        final_score = running_sum / (total_pairs * num_classifiers)
    else:
        final_score = running_sum

        # --- report
    print("[RESULT] SUMMARY:")
    print(f"Images evaluated      : {total_pairs}")
    print(f"Classifiers considered: {num_classifiers}")
    print(f"Final score           : {final_score:.6f}")

    for name, pack in classifiers.items():
        acc = np.mean(pack['indicators']) if pack['indicators'] else 0.0
        mean_ssim = np.mean(pack['ssim_vals']) if pack['ssim_vals'] else 0.0
        print(f"[{name:<15}]  attack_success={acc:.4f}  mean_ssim={mean_ssim:.4f}")

    # optional JSON
    out_json = cfg.get('save_json')
    if out_json:
        report = {
            'final_score': final_score,
            'images_evaluated': total_pairs,
            'per_classifier': {
                n: {
                    'attack_success': float(np.mean(c['indicators']) if c['indicators'] else 0.0),
                    'mean_ssim': float(np.mean(c['ssim_vals']) if c['ssim_vals'] else 0.0)
                } for n, c in classifiers.items()
            }
        }
        with open(out_json, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"[RESULT] Detailed report written to {out_json}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Evaluate adversarial images (config-only).")
    parser.add_argument('--config', required=True, help="Path to YAML configuration file.")
    args = parser.parse_args()

    config = load_cfg(args.config)
    evaluate(config)
