#!/usr/bin/env python3
"""
Kindle Screenshot CLI Tool

An ADB‑based automation to capture Kindle pages, swipe, and combine into a PDF.
Includes automatic cropping to remove bottom elements like "5mins left in chapter".

Usage:
    python kindle_screenshot_cli.py
    (Now interactive — works great when double-clicked as a .exe)

Packaging:
    pip install pyinstaller
    pyinstaller --onefile kindle_screenshot_cli.py
"""

import os
import sys
import time
import subprocess
import shutil
from PIL import Image
import img2pdf


def check_adb_connection():
    try:
        output = subprocess.check_output(["adb", "devices"], stderr=subprocess.DEVNULL).decode()
        lines = [l for l in output.splitlines() if l.strip()]
        devices = [l for l in lines[1:] if "device" in l and not l.startswith("List")]
        if not devices:
            print("❌ No device connected. Please connect your Android device with USB debugging ON.")
            input("Press Enter to exit...")
            sys.exit(1)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ adb command not found. Please install Android Platform Tools and ensure adb is on your PATH.")
        input("Press Enter to exit...")
        sys.exit(1)


def clear_directory(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path, exist_ok=True)


def beep():
    if os.name == 'nt':
        try:
            import winsound
            winsound.Beep(1000, 500)
        except ImportError:
            pass
    else:
        sys.stdout.write('\a')
        sys.stdout.flush()


def swipe_next():
    subprocess.call(["adb", "shell", "input", "swipe", "800", "500", "200", "500", "300"], stderr=subprocess.DEVNULL)


def capture_and_crop_page(raw_path, final_path):
    subprocess.call(["adb", "shell", "screencap", "-p", "/sdcard/screen.png"], stderr=subprocess.DEVNULL)
    subprocess.call(["adb", "pull", "/sdcard/screen.png", raw_path], stderr=subprocess.DEVNULL)

    with Image.open(raw_path) as img:
        width, height = img.size
        cropped = img.crop((0, 0, width, int(height * (11 / 11.5))))
        cropped.save(final_path)

    os.remove(raw_path)


def convert_to_pdf(image_dir, output_pdf):
    images = sorted(
        [os.path.join(image_dir, f) for f in os.listdir(image_dir) if f.lower().endswith('.png')]
    )
    if not images:
        print("❌ No images found to convert.")
        return
    with open(output_pdf, 'wb') as f:
        f.write(img2pdf.convert(images))
    print(f"\n✅ PDF saved as: {output_pdf}")
    beep()


def main():
    print("📚 Kindle Screenshot Tool (Interactive Mode)\n")

    # Prompt user for values
    try:
        pages = int(input("Enter number of pages to capture [default 100]: ") or 100)
    except ValueError:
        pages = 100

    try:
        delay = float(input("Delay between page turns (seconds) [default 2.0]: ") or 2.0)
    except ValueError:
        delay = 2.0

    directory = input("Directory to save screenshots [default 'screenshots']: ") or "screenshots"
    output_pdf = input("Name of output PDF file [default 'kindle_capture.pdf']: ") or "kindle_capture.pdf"
    
    clear_choice = input("Clear existing screenshot directory? (y/N): ").strip().lower()
    should_clear = clear_choice == 'y'

    check_adb_connection()

    if should_clear:
        clear_directory(directory)
    else:
        os.makedirs(directory, exist_ok=True)

    print("\n📷 Starting capture process...")
    try:
        for i in range(pages):
            raw_filename = os.path.join(directory, f"raw_{i + 1:03}.png")
            final_filename = os.path.join(directory, f"page_{i + 1:03}.png")

            capture_and_crop_page(raw_filename, final_filename)

            print(f"Captured page {i + 1}/{pages}")
            swipe_next()
            time.sleep(delay)
    except KeyboardInterrupt:
        print("\n🛑 Process interrupted by user.")

    print("\n🧾 Converting to PDF...")
    convert_to_pdf(directory, output_pdf)

    input("\n✅ Done. Press Enter to close...")


if __name__ == '__main__':
    main()
