#!/bin/bash
# Complete H100 Setup Script
# Run this on your H100 server to set up everything

set -e  # Exit on any error

echo "🚀 H100 Complete Setup Starting..."

# Check if H100 GPU is available
echo "🔍 Checking H100 GPU..."
nvidia-smi

# Install NVIDIA Container Toolkit (if not installed)
echo "📦 Installing NVIDIA Container Toolkit..."
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list

sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo systemctl restart docker

# Test GPU access in Docker
echo "🧪 Testing GPU access in Docker..."
docker run --rm --gpus all nvidia/cuda:12.1.0-base-ubuntu22.04 nvidia-smi

# Install Python dependencies
echo "🐍 Installing Python dependencies..."
pip install -r requirements.txt
pip install -r requirements_api.txt

# Make training scripts executable
chmod +x h100_training_commands.sh
chmod +x h100_docker_commands.sh

echo "✅ H100 setup complete!"
echo ""
echo "🎯 Next steps:"
echo "1. Run training: ./h100_training_commands.sh"
echo "2. Build Docker: ./h100_docker_commands.sh"
echo "3. Test API: curl http://localhost:8000/health"
