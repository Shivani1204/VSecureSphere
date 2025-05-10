# Base image: Kali Linux rolling
FROM kalilinux/kali-rolling:latest

# Avoid interactive prompts during builds
ENV DEBIAN_FRONTEND=noninteractive

# Install required tools and desktop environment
RUN apt-get update && apt-get install -y \
    xfce4 \
    xfce4-terminal \
    tigervnc-standalone-server \
    tigervnc-common \
    x11vnc \
    xvfb \
    x11-xserver-utils \
    dbus-x11 \
    iputils-ping \
    net-tools \
    curl \
    wget \
    git \
    python3-websockify \
    nmap \
    hping3 \
    netcat-openbsd \
    metasploit-framework \
    hydra \
    sudo \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Create VNC password directory
RUN mkdir -p ~/.vnc && echo "VSecureSphere" | vncpasswd -f > ~/.vnc/passwd && chmod 600 ~/.vnc/passwd

# Install and configure noVNC
RUN git clone https://github.com/novnc/noVNC.git /opt/noVNC && \
    cd /opt/noVNC && \
    git checkout v1.3.0 && \
    ln -s vnc_lite.html index.html

# Expose VNC and noVNC ports
EXPOSE 5900 6080

# Startup script to launch desktop, VNC server, and noVNC
CMD ["sh", "-c", "Xvfb :1 -screen 0 1024x768x16 & \
                  export DISPLAY=:1 && \
                  startxfce4 & \
                  x11vnc -display :1 -usepw -forever -listen 0.0.0.0 -rfbport 5900 -shared & \
                  /opt/noVNC/utils/novnc_proxy --vnc localhost:5900 --listen 6080"]

