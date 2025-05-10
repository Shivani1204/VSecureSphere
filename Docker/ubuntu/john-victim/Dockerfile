FROM ubuntu:latest

ENV DEBIAN_FRONTEND=noninteractive

# Install GUI, Apache, VNC, and noVNC dependencies
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
    apache2 \
    openssl \
    python3-websockify \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set VNC password
RUN mkdir -p /root/.vnc && echo "VSecureSphere" | vncpasswd -f > /root/.vnc/passwd && chmod 600 /root/.vnc/passwd

# Setup noVNC
RUN git clone https://github.com/novnc/noVNC.git /opt/noVNC && \
    cd /opt/noVNC && ln -s vnc_lite.html index.html

# Create password hash and serve it
RUN echo "shivani:password123" > /root/password.txt && \
    HASH=$(openssl passwd -6 password123) && \
    echo "shivani:$HASH" > /var/www/html/hash.txt

# Expose ports
EXPOSE 5900 6080 80

# Start everything in the right sequence
CMD bash -c "\
    service apache2 start && \
    Xvfb :1 -screen 0 1024x768x16 & \
    export DISPLAY=:1 && \
    sleep 3 && \
    startxfce4 & \
    sleep 5 && \
    x11vnc -display :1 -rfbport 5900 -usepw -forever -shared -bg && \
    /opt/noVNC/utils/novnc_proxy --vnc localhost:5900 --listen 6080"

