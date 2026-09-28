FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# 1. 系統工具 + ripgrep + vscode 使用者（固定 UID/GID 1000，對應 WSL 的一般使用者）
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    iputils-ping \
    curl \
    wget \
    net-tools \
    git \
    ripgrep \
    sudo \
    && groupadd --gid 1000 vscode \
    && useradd --uid 1000 --gid 1000 -m -s /bin/bash vscode \
    && echo "vscode ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/vscode \
    && chmod 0440 /etc/sudoers.d/vscode \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 2. 先複製依賴檔，讓 Docker 快取這一層（程式碼改動不會重裝套件）
COPY requirements.txt .
RUN pip install -r requirements.txt

# 3. 複製專案原始碼（dev container 會把工作區掛載進來覆蓋，這行主要給正式部署用）
COPY --chown=vscode:vscode . .

EXPOSE 8000

USER vscode

CMD ["uvicorn", "src.auth_module.main:app", "--host", "0.0.0.0", "--port", "8000"]