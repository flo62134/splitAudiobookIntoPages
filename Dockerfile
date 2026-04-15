# Dockerfile
FROM node:20-bookworm-slim

ENV DEBIAN_FRONTEND=noninteractive

# System deps: Python, ffmpeg, and BeautifulSoup from Debian (avoids PEP 668)
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-bs4 \
    ffmpeg \
    ca-certificates \
  && rm -rf /var/lib/apt/lists/*

# Echogarden CLI
ARG ECHOGARDEN_VERSION=latest
RUN npm i -g "echogarden@${ECHOGARDEN_VERSION}"

WORKDIR /app
COPY main.py README.md ./

# Pre-create output dirs (still OK to bind mount)
RUN mkdir -p ./alignment ./audiobook_pages

CMD ["python3", "main.py"]
