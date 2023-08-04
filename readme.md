[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

# Fujifilm Model - Exiftool GUI Converter

Python GUI to change the camera model on Fujifilm cameras ( especially older models ) to an X-T4 so the following simulations can be used:

-    Eterna
-    Eterna Bleach Bypass
-    Classic Negative
-    Acros
-    Acros + ( Red / Yellow / Green - Filter )

For example if you have a Fujifilm X100, X-E1, X-E2 or an X70 but want to use Classic Chrome or Eterna Bleach Bypass, you now can.

### Requirements

-- Python 3.6 or higher

-- Exiftool

-- PyQt6

---

### Installation

#### Check your version of Python and upgrade if necessary

```bash
python3 --version
```

#### Clone repository

```bash
git clone https://github.com/BlackCursive/fujifilm-profile-gui-exiftool.git
cd fujifilm-profile-gui-exiftool
```

### Virtual Environment - Install Pipenv using Homebrew or Python

#### macOS

```bash
brew install pipenv
```

or

#### Python

```bash
pip3 install pipenv
```

### Activate Pipenv Shell

```bash
pipenv shell
```

### Install requirements

```bash
pip install PyQt6
```

### Usage - Be sure to place Fujifilm \*.raf files in the raf_files directory or the program will abort

```bash
python3 gui_exifcli.py
```

### Exit Pipenv Shell

```bash
exit
```

### If you run into a permission denied error.

```bash
cd exiftool
sudo chmod 755 exiftool
cd ..
```

---

## Sample Output

![ExifCli](https://github.com/BlackCursive/fujifilm-profile-exiftool/blob/main/gui_exifcli.gif)

---

This project is built with ![Exiftool](https://github.com/exiftool) by Phil Harvey.

-    ExifTool is a platform-independent Perl library plus a command-line application for reading, writing and editing meta information in a wide variety of files.

Also, the base code for the converter used was created by Khuzaima and Faisal Nazik. ![WebP Converter](https://github.com/kzmfhm/pyqt6-webp-file-converter)
