# Use Kali Linux as the base image
FROM kalilinux/kali-rolling

ENV DEBIAN_FRONTEND=noninteractive

# Create a non-root user with sudo access
RUN useradd -m -s /bin/bash attacker && \
    echo "attacker ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

# Update Kali and install vulnerable services
RUN apt-get update && apt-get install -y \
    openssh-server \
    apache2 \
    vsftpd \
    mysql-server \
    samba \
    nmap \
    netcat \
    xvfb \
    x11vnc \
    novnc \
    websockify \
    xfce4 \
    xfce4-terminal \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Configure SSH with weak credentials
RUN echo 'attacker:password' | chpasswd

# Set up VNC password
RUN mkdir -p /home/attacker/.vnc && \
    echo "VSecureSphere" | vncpasswd -f > /home/attacker/.vnc/passwd && \
    chmod 600 /home/attacker/.vnc/passwd && \
    chown -R attacker:attacker /home/attacker/.vnc

# Expose vulnerable services
EXPOSE 22 80 443 3306 21 5900 6080

# Switch to non-root user
USER attacker
WORKDIR /home/attacker

# Start VNC, noVNC, and vulnerable services
CMD ["sh", "-c", "Xvfb :1 -screen 0 1024x768x16 & \
                  export DISPLAY=:1 && \
                  startxfce4 & \
                  x11vnc -display :1 -usepw -forever -listen 0.0.0.0 -rfbport 5900 -shared & \
                  websockify --web=/usr/share/novnc/ 6080 localhost:5900 & \
                  sudo service ssh start && sudo service apache2 start && sudo service mysql start && sudo service vsftpd start && tail -f /dev/null"]

