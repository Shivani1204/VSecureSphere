# Use the latest Ubuntu base image
FROM ubuntu:latest

# Set environment variables to suppress prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install necessary packages including XFCE, VNC, network tools (ifconfig, ping), and git for noVNC
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
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set the VNC password (replace 'mypassword' with your desired password)
RUN mkdir -p ~/.vnc && echo "VSecureSphere" | vncpasswd -f > ~/.vnc/passwd && chmod 600 ~/.vnc/passwd

# Install noVNC and configure it
RUN git clone https://github.com/novnc/noVNC.git /opt/noVNC && \
    cd /opt/noVNC && \
    git checkout v1.3.0 && \
    ln -s vnc_lite.html index.html

# Expose ports for VNC (5900) and noVNC (6080)
EXPOSE 5900 6080

# Start the VNC server, noVNC, and websockify when the container starts
CMD ["sh", "-c", "Xvfb :1 -screen 0 1024x768x16 & \
                  export DISPLAY=:1 && \
                  startxfce4 & \
                  x11vnc -display :1 -usepw -forever -listen 0.0.0.0 -rfbport 5900 -shared & \
                  /opt/noVNC/utils/novnc_proxy --vnc localhost:5900 --listen 6080"]
