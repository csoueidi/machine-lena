# Installation Instructions

## Project Dependencies Successfully Installed ✓

This document summarizes the dependencies for "The Machine" project.

### Python Dependencies

All Python dependencies have been installed using pip3 with the `--user` and `--break-system-packages` flags (required for Raspberry Pi OS).

#### Installed Packages:
1. **antlr4-python3-runtime==4.13.0** - ANTLR parser runtime for choreography language
2. **flask** - Web framework for the service API
3. **flask-cors** - CORS support for Flask applications
4. **opencv-python** - Computer vision library for camera/motion detection
5. **numpy** - Numerical computing (already installed system-wide)
6. **RPi.GPIO** - Raspberry Pi GPIO control library
7. **picamera2** - Raspberry Pi camera interface (already installed system-wide)
8. **websockets** - WebSocket client/server for real-time communication
9. **pyyaml** - YAML configuration file parser (already installed system-wide)

### System Requirements

This project runs on Raspberry Pi OS and requires:
- Python 3.7 or higher
- Java Runtime (for ANTLR grammar compilation)
- 24V DC power supply for motor controllers
- Camera module connected to Raspberry Pi

### Additional Notes

⚠️ **Important**: The installation script added packages to `/home/pi/.local/bin` which may not be on your PATH. Consider adding it:

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### Running the Project

Based on the README, you can run the different modules:

1. **Service Module** (Main choreography controller):
   ```bash
   cd /home/pi/Code/machine/service
   python3 app.py
   ```

2. **UI Module** (Web interface):
   ```bash
   cd /home/pi/Code/machine/ui
   python3 -m http.server 8003
   ```

3. **Installation Module** (Motion detection + choreography):
   ```bash
   cd /home/pi/Code/machine/installation
   python3 combined.py
   ```

### Compiling ANTLR Grammars (if needed)

If you need to recompile the choreography grammar:
```bash
cd /home/pi/Code/machine
java -jar binaries/antlr-4.13.1-complete.jar -Dlanguage=Python3 -no-listener -visitor choreography/Choreography.g4
```

### Configuration

Motor configuration is stored in:
- `/home/pi/Code/machine/config/config1.yaml`

Make sure to adjust the configuration according to your hardware setup.

### Troubleshooting

If you encounter any GPIO permission issues, make sure your user is in the `gpio` group:
```bash
sudo usermod -a -G gpio pi
```

For camera issues, ensure the camera is enabled in `raspi-config`.
