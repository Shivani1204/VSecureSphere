# ---- Stage 1: Build Stage ----
FROM ubuntu:latest AS builder

ENV DEBIAN_FRONTEND=noninteractive

# Update packages and install dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    git \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Ensure 'python' points to 'python3'
RUN ln -s /usr/bin/python3 /usr/bin/python

# Create a virtual environment and install SQLMap
RUN python3 -m venv /opt/sqlmap-env && \
    /opt/sqlmap-env/bin/pip install --no-cache-dir sqlmap

# ---- Stage 2: Final Minimal Image ----
FROM ubuntu:latest

ENV DEBIAN_FRONTEND=noninteractive

# Install only necessary runtime dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-venv \
    xfce4 \
    xfce4-terminal \
    tigervnc-standalone-server \
    x11vnc \
    xvfb \
    iputils-ping \
    net-tools \
    curl \
    wget \
    sudo \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Ensure 'python' points to 'python3'
RUN ln -s /usr/bin/python3 /usr/bin/python

# Copy SQLMap from the builder stage
COPY --from=builder /opt/sqlmap-env /opt/sqlmap-env

# Set environment variables to use the virtual environment
ENV PATH="/opt/sqlmap-env/bin:$PATH"

# Verify SQLMap installation
RUN sqlmap --version

# Expose ports for VNC and noVNC
EXPOSE 5900 6080

# Start services on container start
CMD ["sh", "-c", "Xvfb :1 -screen 0 1024x768x16 & \
                  export DISPLAY=:1 && \
                  startxfce4 & \
                  x11vnc -display :1 -usepw -forever -listen 0.0.0.0 -rfbport 5900 -shared & \
                  /opt/noVNC/utils/novnc_proxy --vnc localhost:5900 --listen 6080"]

