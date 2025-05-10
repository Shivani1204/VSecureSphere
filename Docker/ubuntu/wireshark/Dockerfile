# Use the latest Ubuntu base image
FROM ubuntu:latest

# Set environment variable to suppress interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install necessary packages
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
    wireshark \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set VNC password and create .vnc directory
RUN mkdir -p ~/.vnc && \
    echo "VSecureSphere" | vncpasswd -f > ~/.vnc/passwd && \
    chmod 600 ~/.vnc/passwd

# Install noVNC and set up the web interface
RUN git clone https://github.com/novnc/noVNC.git /opt/noVNC && \
    cd /opt/noVNC && \
    git checkout v1.3.0 && \
    ln -s vnc_lite.html index.html

# Expose ports for VNC and noVNC
EXPOSE 5900 6080

# Create a start script to handle launching XFCE, VNC, and noVNC
RUN echo "#!/bin/bash\n\
export DISPLAY=:1\n\
xrdb $HOME/.Xresources\n\
Xvfb :1 -screen 0 1024x768x16 &\n\
sleep 2\n\
startxfce4 > /dev/null 2>&1 &\n\
x11vnc -display :1 -usepw -forever -listen 0.0.0.0 -rfbport 5900 -shared &\n\
/opt/noVNC/utils/novnc_proxy --vnc localhost:5900 --listen 6080 &\n\
tail -f /dev/null" > /start.sh

# Make start script executable
RUN chmod +x /start.sh

# Set the default command to execute the start script
CMD ["/start.sh"]

