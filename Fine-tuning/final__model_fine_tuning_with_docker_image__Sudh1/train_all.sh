#!/bin/bash
# Train All Models Script
# Run this to train all 5 models

echo "🚀 Starting All Model Training"
echo "================================"

# Set environment variables for optimal performance
export CUDA_VISIBLE_DEVICES=0
export PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512
export TOKENIZERS_PARALLELISM=false

echo ""
echo "📊 Training HR Model (Full Fine-tuning)..."
python finetuning/full_finetuning.py

echo ""
echo "🏥 Training Healthcare Model (LoRA)..."
python finetuning/lora_finetuning.py

echo ""
echo "🛒 Training Sales Model (PEFT)..."
python finetuning/peft_finetuning.py

echo ""
echo "📢 Training Marketing Model (QLoRA)..."
python finetuning/qlora_finetuning.py

echo ""
echo "💰 Training Finance Model (DPO)..."
python finetuning/dpo_finetuning.py

echo ""
echo "✅ All training completed!"
echo "📁 Models saved in: models/"
