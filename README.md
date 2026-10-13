# 🤖 Arduino Servo Motor Controller Website

A web-based servo motor controller that allows users to control a physical SG90 servo motor using a slider on a website through a smartphone or laptop.

## 🚀 Project Overview

This project connects a web interface with an Arduino Uno to control a servo motor's angle in real time. A Flask web server receives the selected angle and sends it to the Arduino through serial communication.

The project helped me understand how web technologies, Python, serial communication, and embedded hardware can work together.

## ✨ Features

- 🎚️ Control servo angles from 0° to 180°
- 📱 Access the control interface from a smartphone
- 🎯 Select precise angles using a slider
- ⚡ Real-time communication between the website and Arduino
- 🦾 Futuristic robotics-inspired user interface
- 🔌 Serial communication between Flask and Arduino

## 🛠️ Technologies Used

- **C++** — Arduino programming
- **Python** — Backend communication
- **Flask** — Web server
- **HTML & CSS** — Website interface
- **JavaScript** — Interactive controls
- **Arduino Uno** — Microcontroller
- **SG90 Servo Motor** — Physical movement
- **Serial Communication** — Website-to-hardware communication

## 🔧 Hardware Requirements

- Arduino Uno
- SG90 Servo Motor
- USB cable
- Laptop and smartphone connected to the same network

## ⚙️ How It Works

1. The Arduino is connected to the laptop through USB.
2. The Flask server runs on the laptop.
3. The smartphone or laptop opens the servo control website.
4. The user selects an angle using the slider.
5. The website sends the angle to the Flask backend.
6. Python sends the angle to the Arduino through serial communication.
7. The Arduino moves the servo motor to the requested position.

## ▶️ How to Run

1. Connect the SG90 servo to the Arduino Uno.
2. Upload the Arduino C++ code.
3. Install Flask and PySerial:

   ```bash
   pip install flask pyserial
   ```

4. Update the serial port in `servoMotor.py` if required.
5. Run the Flask application:

   ```bash
   python servoMotor.py
   ```

6. Open the website using the laptop's local network IP address and port `5000`.
7. Move the slider and observe the servo motor respond.

**Note:** Keep the Arduino's serial communication baud rate and the Python serial configuration synchronized. Close the Arduino Serial Monitor before running the Flask application.

## 📚 What I Learned

- Controlling physical hardware through a web interface
- Understanding serial communication between Python and Arduino
- Building an interactive website with Flask
- Connecting embedded systems with software applications
- Debugging communication issues between hardware and software

## 🔮 Future Improvements

- Add more servo motors
- Display live angle and connection status
- Add saved angle presets
- Explore IoT-based remote control

## 👩‍💻 Author

**Monalisa B. S.**

Computer Science and Engineering Student

Building projects to learn by understanding, experimenting, and connecting software with hardware.
