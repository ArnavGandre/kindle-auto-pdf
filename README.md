# Kindle Screenshot CLI Tool

An Android Debug Bridge (ADB) automation tool to capture Kindle pages, swipe between them, and combine the captures into a single PDF. It automatically crops the bottom elements (like "5mins left in chapter") for a clean reading experience.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.x** - The programming language used for this tool
- **ADB (Android Debug Bridge)** - For communicating with your Kindle device
- **PIL (Python Imaging Library)** - For image processing
- **img2pdf** - For converting images to PDF

## Installation

1. **Install Python Dependencies**:
   ```bash
   pip install pillow img2pdf
   ```

2. **Install ADB**:
   - **Windows**: Download and install [Android Platform Tools](https://developer.android.com/studio/releases/platform-tools)
   - **macOS**: `brew install android-platform-tools`
   - **Linux**: `sudo apt install adb`

3. **Ensure ADB is in your PATH**:
   - After installing ADB, make sure it's accessible from your command line by typing `adb version`
   - If it's not recognized, add the platform-tools directory to your system PATH

4. **Set up your Kindle device**:
   - Enable Developer Options by going to Settings > Device Options and tapping "Serial Number" 7 times
   - Turn on USB Debugging in Developer Options
   - Connect your device to the computer via USB
   - Allow USB debugging when prompted on your device

## Basic Usage

1. Run the script:
   ```bash
   python kindle_screenshot_cli.py
   ```

2. Follow the interactive prompts:
   - Number of pages to capture
   - Delay between page turns
   - Directory to save screenshots
   - Name of output PDF file
   - Whether to clear existing screenshot directory

3. The tool will:
   - Capture screenshots of each page
   - Crop them to remove bottom elements
   - Save them to the specified directory
   - Convert them to a single PDF

## Parameter Customization

The tool offers several parameters you can modify through the interactive interface:

| Parameter | Description | Default | How to Modify |
|-----------|-------------|---------|---------------|
| `pages` | Number of pages to capture | 100 | Enter a different number when prompted |
| `delay` | Seconds between page turns | 2.0 | Increase for slower page turns or decrease for faster capturing |
| `directory` | Folder to save screenshots | "screenshots" | Specify a different path when prompted |
| `output_pdf` | Name of the final PDF file | "kindle_capture.pdf" | Enter a different filename when prompted |
| `should_clear` | Whether to delete existing files | False | Enter 'y' when prompted to clear existing directory |

## Code Modification Guide

If you want to modify the code directly rather than using the interactive interface, here are the key sections:

### Swipe Parameters

In the `swipe_next()` function:

```python
def swipe_next():
    subprocess.call(["adb", "shell", "input", "swipe", "800", "500", "200", "500", "300"], stderr=subprocess.DEVNULL)
```

The parameters are:
- `800, 500`: Starting X,Y coordinates for the swipe
- `200, 500`: Ending X,Y coordinates
- `300`: Duration of swipe in milliseconds

For different devices or swipe behaviors, adjust these coordinates and duration.

### Cropping Ratio

In the `capture_and_crop_page()` function:

```python
cropped = img.crop((0, 0, width, int(height * (11 / 11.5))))
```

The `11 / 11.5` ratio determines how much of the bottom to crop:
- Increase the denominator (e.g., `11 / 12.0`) to crop more
- Decrease it (e.g., `11 / 11.2`) to crop less
- Change to `1.0` to disable cropping completely

### Default Values

At the beginning of the `main()` function:

```python
pages = int(input("Enter number of pages to capture [default 100]: ") or 100)
delay = float(input("Delay between page turns (seconds) [default 2.0]: ") or 2.0)
directory = input("Directory to save screenshots [default 'screenshots']: ") or "screenshots"
output_pdf = input("Name of output PDF file [default 'kindle_capture.pdf']: ") or "kindle_capture.pdf"
```

Modify the default values in these lines to change the script's default behavior.

## Building an Executable

To create a standalone executable:

1. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```

2. Create the executable:
   ```bash
   pyinstaller --onefile kindle_screenshot_cli.py
   ```

3. Find the executable in the `dist` directory

## Troubleshooting

- **"No device connected"**: Ensure your Kindle is connected and USB debugging is enabled
- **"adb command not found"**: Make sure ADB is installed and in your PATH
- **Captures not working**: Try increasing the delay between page turns
- **Images not appearing in the PDF**: Check if images were captured correctly in the screenshots directory

## Advanced Usage

### Silent Mode

To run the script with preset values and no prompts, modify the `main()` function:

```python
def main():
    # Replace interactive input with hard-coded values
    pages = 100
    delay = 2.0
    directory = "screenshots"
    output_pdf = "kindle_capture.pdf"
    should_clear = True
    
    check_adb_connection()
    
    if should_clear:
        clear_directory(directory)
    else:
        os.makedirs(directory, exist_ok=True)
    
    # Rest of the function remains the same...
```

### Custom Crop Areas

To crop specific areas (like removing headers as well as footers), modify the crop parameters:

```python
# To crop both top and bottom:
top_margin = int(height * 0.05)  # 5% from top
bottom_margin = int(height * 0.95)  # 5% from bottom
cropped = img.crop((0, top_margin, width, bottom_margin))
```

## License

This tool is shared for educational purposes. Use responsibly and respect copyright laws when capturing content.
