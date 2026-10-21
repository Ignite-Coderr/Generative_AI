# 🚀 ChatGPT (Open WebUI) — EC2 Deployment & Monitoring

## 🌟 Overview
This project deploys an Open WebUI (ChatGPT-like) instance on AWS EC2, enabling user registration, multi-model access, and real-time monitoring with Grafana + OTEL.

## 📁 Repository Layout
- 🔑 `aman_euri_new.ppk` — SSH key (PuTTY) for EC2 access
- 🟢 `open_webui_monitoring_json_9SsY.json` — Grafana dashboard config
- 📄 `Openwebui_ec2_setup_and_monitoring_docx_gm4U.docx` — Setup notes & instructions

## 🛠️ Prerequisites
- AWS EC2 instance (Ubuntu recommended)
- Security group: allow inbound TCP for ports 8000 (Open WebUI), 3000 (Grafana), 4317/4318 (OTEL)
- Docker Engine & Docker Compose (v2)

## ⚡ Quick Deployment (EC2 Ubuntu)
1. SSH into your EC2 instance:
   ```bash
   ssh -i "path/to/key.pem" ubuntu@<EC2_PUBLIC_IP>
   ```
2. Clone/copy project files to the instance.
3. Start containers:
   ```bash
   sudo docker compose -f docker-compose.otel.yaml up -d
   ```
4. Verify containers:
   ```bash
   docker ps
   ```

### 🐳 Docker Troubleshooting
- Permission denied? Add user to docker group:
  ```bash
  sudo usermod -aG docker ubuntu
  newgrp docker
  docker ps
  ```

## 🪟 Windows (PowerShell) Notes
- Use WinSCP/Putty for PPK keys or OpenSSH for SCP:
  ```powershell
  scp -i "C:\path\to\key.pem" .\open_webui_monitoring_json_9SsY.json ubuntu@<EC2_PUBLIC_IP>:/home/ubuntu/
  ```

## 🌐 Access URLs
- WebUI: [http://<EC2_PUBLIC_IP>:8000](http://<EC2_PUBLIC_IP>:8000)
- Grafana: [http://<EC2_PUBLIC_IP>:3000](http://<EC2_PUBLIC_IP>:3000)

## 👤 User Registration & Models
- Supports user registration (if enabled). See `Openwebui_ec2_setup_and_monitoring_docx_gm4U.docx` for config/auth details.

## 📈 Grafana & OTEL
- Grafana is bundled or can run separately. Import `open_webui_monitoring_json_9SsY.json` for dashboards.
- Ensure OTEL collector ports (4317/4318) are open and Grafana can read telemetry.

## 🛑 Troubleshooting
- Docker permission errors: see above
- Images not showing? Place screenshots in `Chatgpt/screenshots/` and use the exact filenames listed.
- Port issues? Check security group rules and port usage.

## 🧰 Useful Commands
- Start: `sudo docker compose -f docker-compose.otel.yaml up -d`
- Stop: `sudo docker compose -f docker-compose.otel.yaml down`
- List containers: `docker ps --format "table {{.ID}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}"`
- Logs: `docker logs -f open-webui`

## 📬 Contact & Next Steps
- Want more features, automation, or help? Open an issue or connect on [LinkedIn](https://www.linkedin.com/in/aman-husain-123/)

---
**Tip:** For images to show, create a `screenshots` folder inside your `Chatgpt` directory and upload your PNGs there!
