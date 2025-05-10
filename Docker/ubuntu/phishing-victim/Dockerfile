# Use Ubuntu 20.04 as base image
FROM ubuntu:20.04

# Avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install necessary packages
RUN apt-get update && apt-get install -y \
    xfce4 \
    xfce4-terminal \
    x11vnc \
    xvfb \
    net-tools \
    iputils-ping \
    curl \
    wget \
    firefox \
    sudo \
    git \
    python3-websockify \
    tigervnc-standalone-server \
    dbus-x11 \
    x11-xserver-utils \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install noVNC
RUN git clone https://github.com/novnc/noVNC.git /opt/noVNC && \
    cd /opt/noVNC && \
    git checkout v1.3.0 && \
    ln -s vnc_lite.html index.html

# Create startup script to fix black screen
RUN echo '#!/bin/bash\n\
export DISPLAY=:1\n\
mkdir -p /root/.vnc\n\
echo "VSecureSphere" | vncpasswd -f > /root/.vnc/passwd\n\
chmod 600 /root/.vnc/passwd\n\
Xvfb :1 -screen 0 1024x768x16 &\n\
sleep 2\n\
dbus-launch startxfce4 &\n\
x11vnc -display :1 -usepw -forever -nopw -shared -rfbport 5900 -listen 0.0.0.0 &\n\
/opt/noVNC/utils/novnc_proxy --vnc localhost:5900 --listen 6080\n' \
> /startup.sh && chmod +x /startup.sh

# Expose ports
EXPOSE 5900 6080

# Run startup script
CMD ["/startup.sh"]

