@echo off
echo 🚀 Starting All Model Training
echo ================================

echo.
echo 📊 Training HR Model (Full Fine-tuning)...
python finetuning/full_finetuning.py

echo.
echo 🏥 Training Healthcare Model (LoRA)...
python finetuning/lora_finetuning.py

echo.
echo 🛒 Training Sales Model (PEFT)...
python finetuning/peft_finetuning.py

echo.
echo 📢 Training Marketing Model (QLoRA)...
python finetuning/qlora_finetuning.py

echo.
echo 💰 Training Finance Model (DPO)...
python finetuning/dpo_finetuning.py

echo.
echo ✅ All training completed!
echo 📁 Models saved in: models/
pause
