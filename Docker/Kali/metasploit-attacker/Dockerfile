# Stage 1: Builder - Install required tools in a temporary container
FROM kalilinux/kali-rolling:latest AS builder

ENV DEBIAN_FRONTEND=noninteractive

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
    postgresql \
    metasploit-framework \
    python3-websockify \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Initialize Metasploit database
RUN service postgresql start && msfdb init

# Clone noVNC (lightweight remote desktop)
RUN git clone --depth=1 https://github.com/novnc/noVNC.git /opt/noVNC && \
    ln -s /opt/noVNC/vnc_lite.html /opt/noVNC/index.html

# Stage 2: Final Image - Copy only essential components from the builder stage
FROM kalilinux/kali-rolling:latest

ENV DEBIAN_FRONTEND=noninteractive

# Install only the runtime dependencies
RUN apt-get update && apt-get install -y \
    xfce4 \
    tigervnc-standalone-server \
    x11vnc \
    xvfb \
    dbus-x11 \
    postgresql \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy Metasploit from the builder stage
COPY --from=builder /usr/share/metasploit-framework /usr/share/metasploit-framework
COPY --from=builder /opt/noVNC /opt/noVNC

# Set up VNC password
RUN mkdir -p ~/.vnc && echo "VSecureSphere" | vncpasswd -f > ~/.vnc/passwd && chmod 600 ~/.vnc/passwd

# Expose VNC and noVNC ports
EXPOSE 5900 6080

# Start services when the container starts
CMD ["sh", "-c", "Xvfb :1 -screen 0 1024x768x16 & \
                  export DISPLAY=:1 && \
                  startxfce4 & \
                  x11vnc -display :1 -usepw -forever -listen 0.0.0.0 -rfbport 5900 -shared & \
                  service postgresql start && \
                  msfconsole & \
                  /opt/noVNC/utils/novnc_proxy --vnc localhost:5900 --listen 6080"]

