#!/bin/bash

# Start vulnerable services
service apache2 start
service ssh start
service vsftpd start

# Start X virtual framebuffer
Xvfb :0 -screen 0 1024x768x16 &
export DISPLAY=:0
sleep 2

# Start desktop environment
startxfce4 &

# Start VNC server
x11vnc -display :0 -usepw -forever -listen 0.0.0.0 -rfbport 5900 -shared &
sleep 2

# Start noVNC proxy
/opt/noVNC/utils/novnc_proxy --vnc localhost:5900 --listen 6080

