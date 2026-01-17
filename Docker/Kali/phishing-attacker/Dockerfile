# Use the latest Kali Linux base image
FROM kalilinux/kali-rolling:latest

ENV DEBIAN_FRONTEND=noninteractive

# Install XFCE desktop, VNC, noVNC tools, SET, and dependencies
RUN apt-get update && apt-get install -y \
    xfce4 xfce4-terminal \
    tigervnc-standalone-server tigervnc-common \
    x11vnc xvfb x11-xserver-utils dbus-x11 \
    net-tools iputils-ping curl wget git \
    python3-websockify sudo apache2 \
    metasploit-framework \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install SET (Social Engineering Toolkit)
RUN git clone https://github.com/trustedsec/social-engineer-toolkit /opt/setoolkit

# Set VNC password
RUN mkdir -p ~/.vnc && echo "VSecureSphere" | vncpasswd -f > ~/.vnc/passwd && chmod 600 ~/.vnc/passwd

# Install noVNC
RUN git clone https://github.com/novnc/noVNC.git /opt/noVNC && \
    cd /opt/noVNC && git checkout v1.3.0 && ln -s vnc_lite.html index.html

# Expose ports for VNC and noVNC
EXPOSE 5900 6080

# Start GUI, x11vnc, and noVNC
CMD ["sh", "-c", "Xvfb :1 -screen 0 1024x768x16 & \
                  export DISPLAY=:1 && \
                  startxfce4 & \
                  x11vnc -display :1 -usepw -forever -listen 0.0.0.0 -rfbport 5900 -shared & \
                  /opt/noVNC/utils/novnc_proxy --vnc localhost:5900 --listen 6080"]

