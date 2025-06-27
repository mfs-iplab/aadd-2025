# AADD-2025: Adversarial Attacks on Deepfake Detectors Challenge

<picture>
  <img alt="Logos" src="/assets/images/headernewaadd.jpg">
</picture>

## 1st Adversarial Attacks on Deepfake Detectors: A Challenge in the Era of AI-Generated Media

**Grand Challenge at [ACM Multimedia 2025](https://acmmm2025.org/)**

---

## 🎯 Overview

The AADD-2025 Challenge investigated adversarial vulnerabilities of deepfake detection models by generating adversarial perturbed deepfake images that evade standard classifiers while maintaining high visual similarity to the original deepfake content. Given the increasing reliance on deepfake detectors in forensic analysis and content moderation, ensuring their robustness against adversarial attacks has relevant importance.

## 🎪 Challenge Description

The goal of this challenge was to expose and address vulnerabilities in current deepfake detection systems by designing adversarial attacks that alter deepfake images, rendering them unrecognizable as synthetic content to 4 proposed classifiers, **preserving high visual similarity** to the original images.

## 📊 Dataset Structure

Participants were provided with a dataset divided into **sixteen subsets**:

### High Quality Resolution:
- **4 GAN-based models** (high quality)
- **4 Diffusion-based models** (high quality)

### Low Quality Resolution:
- **4 GAN-based models** (low quality)
- **4 Diffusion-based models** (low quality)

```
- Dataset
├── train
│   ├── fake
│   │   ├── hq
│   │   │   ├── Adobe Firefly
│   │   │   ├── Deep AI
│   │   │   ├── Flux.1.1 Pro
│   │   │   ├── Hotpot AI
│   │   │   ├── Nvidia Sana PAG
│   │   │   ├── Stable Diffusion 3.5
│   │   │   ├── StyleGAN2
│   │   │   ├── StyleGAN3
│   │   │   └── Tencent Hunyuan
│   │   └── lq
│   │       ├── Deep AI
│   │       ├── Flux.1
│   │       ├── Freepik
│   │       ├── Hotpot AI
│   │       ├── Nvidia Sana PAG
│   │       ├── Stable Diffusion Attend and Excite
│   │       ├── StyleGAN
│   │       ├── StyleGAN3
│   │       └── Tencent Hunyuan
│   └── real
│       ├── hq
│       │   └── ffhq
│       └── lq
│           └── celeba_hq
└── test
    ├── fake
    │   ├── hq
    │   │   ├── Adobe Firefly
    │   │   ├── Deep AI
    │   │   ├── Flux.1.1 Pro
    │   │   ├── Hotpot AI
    │   │   ├── Nvidia Sana PAG
    │   │   ├── Stable Diffusion 3.5
    │   │   ├── StyleGAN2
    │   │   ├── StyleGAN3
    │   │   └── Tencent Hunyuan
    │   └── lq
    │       ├── Deep AI
    │       ├── Flux.1
    │       ├── Freepik
    │       ├── Hotpot AI
    │       ├── Nvidia Sana PAG
    │       ├── Stable Diffusion Attend and Excite
    │       ├── StyleGAN
    │       ├── StyleGAN3
    │       └── Tencent Hunyuan
    └── real
        ├── hq
        │   └── ffhq
        └── lq
            └── celeba_hq
```

**Note**: Participants had to focus on the entire dataset across all subsets.

## 📋 Submission Requirements

1. **Adversarial Images**: Submit the generated adversarial deepfake images
2. **Technical Abstract**: Provide a detailed description of your methodology
3. **Results Documentation**: Include performance metrics and analysis

## 📥 Evaluation Resources

**Final Evaluation Scripts** [See here](scripts)

## 🏆 Results & Rankings

The challenge ended with strong global participation. Here are the final standings:

| Rank | Team Name | Organization/Institution | Final Score |
|------|-----------|-------------------------|-------------|
| 🥇 1st | **MR-CAS** | University of Chinese Academy of Sciences | **2740** |
| 🥈 2nd | **Safe AI** | UNIST (Ulsan National Institute of Science and Technology) | **2709** |
| 🥉 3rd | **RoMa** | Fraunhofer SIT \| ATHENE Center | **2679** |
| 4th | GRADIANT | Gradiant | 2631 |
| 5th | DASH | Sungkyunkwan University | 2618 |
| 6th | SecureML | University of Cagliari | 2490 |
| 7th | MICV | Ant Group | 2434 |
| 8th | WHU_PB | Wuhan University | 2354 |
| 9th | The Adversaries | Singapore Institute of Technology | 2341 |
| 10th | DeFakePol | Samsung Research Poland | 1665 |
| 11th | False Negative | The Hong Kong Polytechnic University | 1602 |
| 12th | VYAKRITI 2.0 | Apex Institute of technology Chandigarh University | 1041 |
| 13th | MILab | University of Science and Technology of China | 110 |

## 📊 Timeline

The AADD-2025 Challenge followed this timeline:

- ✅ **March 03, 2025**: Competition Website Launch  
- ✅ **March 15 - May 22, 2025**: Registration Period (Extended)
- ✅ **April 10, 2025**: Test Set and Classificator Release  
- ✅ **June 15, 2025**: Final Submission Deadline  
- ✅ **June 22, 2025**: Leaderboard Publication and Rankings Release
- ⏳ **June 30, 2025**: Paper Submission Deadline (Top 3 Teams Only)
- ⏳ **July 24, 2025**: Announcement regarding full paper submission
- ⏳ **August 01, 2025**: Camera ready - Grand Challenge Solutions (Top 3 Teams Only)
- ⏳ **ACM Multimedia 2025**: Conference & Winners Recognition

## 📝 Publication Opportunities

The top 3 teams were invited to submit full-length papers describing their methods in detail. These papers underwent a rigorous review process managed by the challenge organizers, with accepted papers included in the ACM Multimedia 2025 proceedings.

## 👥 Organizing Committee

### Chairs
| Name | Role | Email | Affiliation |
|------|------|-------|-------------|
| **Luca Guarnera** | Research Fellow | luca.guarnera@unict.it | Department of Mathematics and Computer Science, University of Catania, Italy |
| **Francesco Guarnera** | Research Fellow | francesco.guarnera@unict.it | Department of Mathematics and Computer Science, University of Catania, Italy |

### Co-Chairs
| Name | Role | Email | Affiliation |
|------|------|-------|-------------|
| **Sebastiano Battiato** | Full Professor | sebastiano.battiato@unict.it | Department of Mathematics and Computer Science, University of Catania, Italy |
| **Giovanni Puglisi** | Associate Professor | puglisi@unica.it | Department of Mathematics and Informatics, University of Cagliari, Italy |
| **Zahid Akhtar** | Associate Professor | akhtarz@sunypoly.edu | State University of New York Polytechnic Institute, USA |

### Technical Committee
| Name | Role | Email | Affiliation |
|------|------|-------|-------------|
| **Mirko Casu** | PhD Student | mirko.casu@phd.unict.it | Department of Mathematics and Computer Science, University of Catania, Italy |
| **Orazio Pontorno** | PhD Student | orazio.pontorno@phd.unict.it | Department of Mathematics and Computer Science, University of Catania, Italy |
| **Claudio Vittorio Ragaglia** | PhD Student | claudio.ragaglia@phd.unict.it | Department of Mathematics and Computer Science, University of Catania, Italy |

## 📧 Contact Information

**Main Contact**: Mirko Casu  
**Email**: challenge.dff@gmail.com 

## 📖 Citation

**Dataset Attribution**: Part of this challenge dataset is based on the WILD dataset. If you use the data, please also cite:

```bibtex
@misc{bongini2025wildnewinthewildimage,
      title={WILD: a new in-the-Wild Image Linkage Dataset for synthetic image attribution}, 
      author={Pietro Bongini and Sara Mandelli and Andrea Montibeller and Mirko Casu and Orazio Pontorno and Claudio Vittorio Ragaglia and Luca Zanchetta and Mattia Aquilina and Taiba Majid Wani and Luca Guarnera and Benedetta Tondi and Giulia Boato and Paolo Bestagini and Irene Amerini and Francesco De Natale and Sebastiano Battiato and Mauro Barni},
      year={2025},
      eprint={2504.19595},
      archivePrefix={arXiv},
      primaryClass={cs.MM},
      url={https://arxiv.org/abs/2504.19595}, 
}
```

## 🌐 Related Resources

- [ACM Multimedia 2025 Conference](https://acmmm2025.org/)
- [Challenge Website](https://iplab.dmi.unict.it/mfs/acm-aadd-challenge-2025/)

**Institutional Affiliations:**
- **University of Catania** - [Department of Mathematics and Computer Science](https://web.dmi.unict.it/en)
- **University of Cagliari** - [Department of Mathematics and Informatics](https://web.unica.it/unica/en/dip_matinfo.page)
- **State University of New York Polytechnic Institute** - [Website](https://sunypoly.edu/)

© 2025 [University of Catania](https://www.unict.it/en).  
Powered by the [Multimedia Security and Forensics](https://iplab.dmi.unict.it/mfs/) group of the [Image Processing Laboratory (IPLAB)](https://iplab.dmi.unict.it/).

## 🏷️ Keywords

`Deepfake Detection`, `Adversarial Attacks`, `Computer Vision`, `Digital Forensics`, `AI Security`, `Media Authentication`, `Challenge Competition`, `ACM Multimedia`

---

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="/assets/images/loghiunictiplab2.png">
  <source media="(prefers-color-scheme: light)" srcset="/assets/images/loghiunictiplabblack.png">
  <img alt="Logos" src="/assets/images/loghiunictiplab2.png">
</picture>
