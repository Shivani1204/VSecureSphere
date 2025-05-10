# Use the latest Ubuntu base image
FROM ubuntu:latest

ENV DEBIAN_FRONTEND=noninteractive

# Install GUI, networking tools, and Snort dependencies
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
    snort \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set VNC password
RUN mkdir -p ~/.vnc && \
    echo "VSecureSphere" | vncpasswd -f > ~/.vnc/passwd && \
    chmod 600 ~/.vnc/passwd

# Install noVNC
RUN git clone https://github.com/novnc/noVNC.git /opt/noVNC && \
    cd /opt/noVNC && \
    git checkout v1.3.0 && \
    ln -s vnc_lite.html index.html

# Expose VNC and noVNC ports
EXPOSE 5900 6080

# Start XFCE + VNC + noVNC
CMD ["sh", "-c", "Xvfb :1 -screen 0 1024x768x16 & \
                  export DISPLAY=:1 && \
                  startxfce4 & \
                  x11vnc -display :1 -usepw -forever -listen 0.0.0.0 -rfbport 5900 -shared & \
                  /opt/noVNC/utils/novnc_proxy --vnc localhost:5900 --listen 6080"]

