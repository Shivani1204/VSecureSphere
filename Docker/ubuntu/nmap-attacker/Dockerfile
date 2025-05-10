# Use the official Nessus image as base
FROM tenableofficial/nessus:latest

# Create necessary directories
RUN mkdir -p /opt/nessus/etc/nessus

# Create a comprehensive nessusd.conf with SSL explicitly disabled
RUN echo "# Nessus daemon configuration\n\
xmlrpc_listen_port = 8834\n\
www_server_only = yes\n\
www_server_ip = 0.0.0.0\n\
www_server_port = 8834\n\
ssl = no\n\
start_web_server = yes\n\
force_pubkey_auth = no\n\
listen_address = 0.0.0.0\n\
allow_header_host = yes" > /opt/nessus/etc/nessus/nessusd.conf

# Expose the Nessus port
EXPOSE 8834

# Run nessusd with the quiet flag
CMD ["/opt/nessus/sbin/nessusd", "-q"]
