FROM mcr.microsoft.com/devcontainers/python:3.12-bookworm

# ffmpeg をインストール
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# devcontainer環境に Docker Compose の使用設定
RUN curl -SL "https://github.com/docker/compose/releases/latest/download/docker-compose-linux-x86_64" -o /usr/local/bin/docker-compose && \
    chmod +x /usr/local/bin/docker-compose

# mise（バージョン管理ツール）をインストール
RUN curl -fsSL https://mise.run | sh && \
    mkdir -p /home/vscode/.local/bin && \ 
    cp /root/.local/bin/mise /home/vscode/.local/bin/ && \
    chown -R vscode:vscode /home/vscode/.local && \
    ln -s /home/vscode/.local/bin/mise /usr/local/bin/mise && \
    chmod +x /usr/local/bin/mise && \
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> /etc/bash.bashrc && \
    echo 'eval "$(mise activate bash)"' >> /etc/bash.bashrc

# git-secrets をインストール
RUN git clone https://github.com/awslabs/git-secrets.git /tmp/git-secrets && \
    cd /tmp/git-secrets && make install && \
    rm -rf /tmp/git-secrets

# PATH を適切に設定
ENV PATH="/root/.local/bin:${PATH}"
