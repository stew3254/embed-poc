#!/usr/bin/env python3
import logging
import os
import sys

from datetime import datetime, timezone
from flask import Flask, render_template, request, send_file
from PIL import Image, ImageDraw, ImageFont

def generate_image(ip):
    # Skip if the image already exists
    if os.path.exists(f"imgs/{ip}.png"):
        return
    # Text and image settings
    image_width = 500
    image_height = 75
    background_color = "black"
    text_color = "white"
    font_size = 64

    # Load font (use default or a .ttf font)
    font = ImageFont.truetype("Inconsolata.otf", font_size)

    # Create image
    img = Image.new("RGB", (image_width, image_height), color=background_color)
    draw = ImageDraw.Draw(img)

    # Get bounding box of the text
    bbox = draw.textbbox((0, 0), ip, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # Calculate position to center the text
    x = (image_width - text_width) / 2
    y = (image_height - text_height) / 2

    # Draw the text
    draw.text((x, y-15), ip, font=font, fill=text_color)

    # Save image
    img.save(f"imgs/{ip}.png")


def get_client_ip(r):
    forwarded_for = r.headers.get('X-Forwarded-For')
    if forwarded_for:
        # Might be a list of IPs: "client, proxy1, proxy2"
        return forwarded_for.split(',')[0].strip()
    return r.remote_addr

app = Flask("Sev1")
log = open("poc.log", "a")

@app.before_request
def log_request_info():
    timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
    ip = get_client_ip(request)
    logging.info(f"[{timestamp}] {request.host} {request.path} {ip}")
@app.route("/")
def index():
    return render_template("index.html", url=request.url_root)

@app.route("/ip.png")
def serve_ip():
    # Get the user's ip
    ip = get_client_ip(request)
    # Generate the image
    generate_image(ip)

    return send_file(f"imgs/{ip}.png", mimetype="image/png")


def main():
    logging.basicConfig(
        filename="poc.log",
        level=logging.INFO,
    )
    # Create the images directory
    os.makedirs("imgs", exist_ok=True)

    port = 1337
    if len(sys.argv) > 1:
        port = int(sys.argv[1])

    app.run(debug=True, host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()
