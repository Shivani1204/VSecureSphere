# Base image: Kali Linux
FROM kalilinux/kali-rolling

ENV DEBIAN_FRONTEND=noninteractive

# Install GUI, noVNC, John the Ripper, and wordlists
RUN apt-get update && apt-get install -y \
    xfce4 \
    xfce4-terminal \
    tigervnc-standalone-server \
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
    john \
    wordlists \
    sudo && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# VNC password
RUN mkdir -p ~/.vnc && echo "VSecureSphere" | vncpasswd -f > ~/.vnc/passwd && chmod 600 ~/.vnc/passwd

# Setup noVNC
RUN git clone https://github.com/novnc/noVNC.git /opt/noVNC && \
    cd /opt/noVNC && ln -s vnc_lite.html index.html

EXPOSE 5900 6080

CMD ["sh", "-c", "Xvfb :1 -screen 0 1024x768x16 & \
                  export DISPLAY=:1 && \
                  startxfce4 & \
                  x11vnc -display :1 -usepw -forever -listen 0.0.0.0 -rfbport 5900 -shared & \
                  /opt/noVNC/utils/novnc_proxy --vnc localhost:5900 --listen 6080"]

