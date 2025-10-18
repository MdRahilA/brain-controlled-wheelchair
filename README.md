# Brain-Controlled Wheelchair (BCW)

![GitHub repo size](https://img.shields.io/github/repo-size/MdRahilA/Brain-Controlled-Wheelchair?color=brightgreen)
![GitHub license](https://img.shields.io/github/license/MdRahilA/Brain-Controlled-Wheelchair)
![GitHub last commit](https://img.shields.io/github/last-commit/MdRahilA/Brain-Controlled-Wheelchair)
![Top language](https://img.shields.io/github/languages/top/MdRahilA/Brain-Controlled-Wheelchair)
![Contributors](https://img.shields.io/github/contributors/MdRahilA/Brain-Controlled-Wheelchair)

![Made with STM32](https://img.shields.io/badge/Made%20with-STM32-blue)
![Category](https://img.shields.io/badge/Category-AI%20%7C%20AssistiveTech-blueviolet)
![Status](https://img.shields.io/badge/Status-Active-success)


A non-invasive **EEG-driven** control system for a powered wheelchair. It decodes brain signals (SSVEP / Motor Imagery) into **Forward / Left / Right / Stop** with strong safety (obstacle override, kill-switch, dead-man stop).

> ⚠️ Research project — not a medical device. Test at low speed, with a handler, in safe areas.

## ✨ Features
- EEG decoding (SSVEP or Motor Imagery)
- Debounced state machine (dwell time + confidence)
- Obstacle safety layer (ultrasonic/LiDAR → auto STOP)
- MCU interface (PWM/ADC or UART/CAN)
- Calibration UI + live plots
- Structured logs for analysis

## 🧱 Architecture






---

## 🧭 System Architecture
<img src="assets/photos/system architecture.png" width="700"/>


## ⚙️ Signal-Processing Pipeline
<img src="assets/photos/system pipeline.png" width="700"/>

## 📸 Project Photos
<p float="left">
  <img src="assets/photos/basic 3D diagram.png" width="340"/>
  <img src="assets/photos/wheelchair.jpg" width="340"/>
</p>

