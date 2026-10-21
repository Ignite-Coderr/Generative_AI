# 🚀 LLM Fine-tuning Project with Indian Datasets

A comprehensive fine-tuning project demonstrating 5 different techniques on Indian domain-specific datasets with complete API deployment, Docker containerization, and Kubernetes orchestration.

## 📊 Fine-tuning Techniques

| Technique | Dataset | Domain | Model Type | Use Case |
|-----------|---------|--------|------------|----------|
| **Full Fine-tuning** | HR Dataset | Employee policies, leave management | Complete parameter training | HR queries, company policies |
| **DPO (Direct Preference Optimization)** | Finance Dataset | Banking, investments, GST | Preference-based training | Financial advice, tax queries |
| **PEFT** | Sales Dataset | Retail, e-commerce, customer service | Parameter-efficient training | Sales strategies, customer support |
| **LoRA** | Healthcare Dataset | Medical queries, Ayurveda | Low-rank adaptation | Medical advice, health queries |
| **QLoRA** | Marketing Dataset | Campaigns, regional strategies | Quantized LoRA | Marketing strategies, campaigns |

## 🏗️ Project Structure

```
finetuningfinal/
├── 📁 datasets/                    # Indian domain datasets
│   ├── hr_dataset.json            # HR policies & leave management
│   ├── finance_dpo_dataset.json   # Banking & investment queries
│   ├── sales_dataset.json         # E-commerce & customer service
│   ├── healthcare_dataset.json     # Medical & Ayurveda queries
│   └── marketing_dataset.json      # Campaign strategies
├── 📁 finetuning/                  # Training scripts
│   ├── full_finetuning.py         # HR model (complete training)
│   ├── dpo_finetuning.py          # Finance model (preference optimization)
│   ├── peft_finetuning.py         # Sales model (parameter-efficient)
│   ├── lora_finetuning.py         # Healthcare model (low-rank adaptation)
│   └── qlora_finetuning.py        # Marketing model (quantized LoRA)
├── 📁 models/                      # Trained model checkpoints
│   ├── hr_full_finetuned/          # HR model outputs
│   ├── finance_dpo_finetuned/     # Finance model outputs
│   ├── sales_peft_finetuned/      # Sales model outputs
│   ├── healthcare_lora_finetuned/ # Healthcare model outputs
│   └── marketing_qlora_finetuned/# Marketing model outputs
├── 🐳 Docker & Deployment
│   ├── Dockerfile                  # Docker configuration
│   ├── docker-compose.yml         # Docker Compose setup
│   ├── kubernetes.yaml            # Kubernetes deployment
│   └── api_server.py              # FastAPI server
├── 🚀 Training Scripts
│   ├── train_all_models.py         # Master training script
│   ├── train_all.bat              # Windows batch file
│   └── train_all.sh               # Linux/H100 script
└── 📋 Configuration
    ├── requirements.txt            # Core dependencies
    ├── requirements_api.txt        # API dependencies
    └── README.md                  # This file
```