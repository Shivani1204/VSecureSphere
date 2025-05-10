FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

# Install desktop environment and tools
RUN apt-get update && apt-get install -y \
    xfce4 \
    x11vnc \
    xvfb \
    wget \
    curl \
    git \
    apache2 \
    vsftpd \
    openssh-server \
    net-tools \
    iputils-ping \
    novnc \
    python3-websockify \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set VNC password
RUN mkdir -p /root/.vnc && \
    x11vnc -storepasswd VSecureSphere /root/.vnc/passwd

# Set up noVNC
RUN git clone https://github.com/novnc/noVNC /opt/noVNC && \
    ln -s /opt/noVNC/vnc_lite.html /opt/noVNC/index.html

# Copy startup script
COPY start.sh /start.sh
RUN chmod +x /start.sh

EXPOSE 5900 6080 21 22 80

CMD ["/start.sh"]

