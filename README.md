# 🚀 VisionFlow-AI

An AI-powered computer vision system for **real-time people detection, tracking, crowd analytics, and movement heatmap generation** using **YOLOv8**, **OpenCV**, and **Python**.

# 🚀 VisionFlow-AI

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)
![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-111F68?style=for-the-badge)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualization-11557C?style=for-the-badge)
![License: MIT](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Platform](https://img.shields.io/badge/Platform-Windows-blue?style=for-the-badge&logo=windows)

The application supports both **live webcam feeds** and **pre-recorded videos**, providing real-time insights into pedestrian movement and crowd behavior.

---

## 📌 Features

- 🎯 Real-time People Detection using YOLOv8
- 👥 Multi-Object Tracking
- 🔥 Dynamic Heatmap Generation
- 🚪 Entry & Exit Counting
- 📊 Crowd Analytics Dashboard
- 📈 Peak & Average Crowd Statistics
- 🎥 Webcam and Video File Support
- 💾 Export Analytics (CSV & JSON)
- 🎬 Save Processed Output Video
- 🧩 Modular Architecture

---

## 🏗️ Project Structure

```
Smart-People-Flow-Analytics-Pro
│
├── Core
│   ├── README.md
│   ├── __init__.py
│   ├── analytics.py
│   ├── dashboard.py
│   ├── detector.py
│   ├── heatmap.py
│   ├── renderer.py
│   ├── tracker.py
│   └── zones.py
│
├── Outputs
│   ├── README.md
│   ├── analytics_summary.csv
│   ├── analytics_summary.json
│   └── processed_video.mp4
│
├── config.py
├── main.py
├── people.mp4
├── requirements.txt
├── LICENSE
├── .gitignore
└── README.md
```

---

## ⚙️ Technologies Used

- Python 3.x
- OpenCV
- Ultralytics YOLOv8
- NumPy
- Pandas
- Matplotlib

---

## 📊 System Workflow

```
Input Video / Webcam
          │
          ▼
YOLOv8 Person Detection
          │
          ▼
Multi-Object Tracking
          │
          ▼
Zone Analysis
          │
          ▼
Heatmap Generation
          │
          ▼
Analytics Engine
          │
          ▼
Dashboard Rendering
          │
          ▼
Output Video + Reports
```

---

## 📦 Installation

Clone the repository

```bash
git clone https://github.com/sri-13-pro/smart-people-flow-analytics-pro.git
```

Navigate to the project

```bash
cd smart-people-flow-analytics-pro
```

Create a virtual environment

```bash
python -m venv venv
```

Activate the virtual environment

**Windows**

```bash
venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Project

### Using Webcam

In `config.py`

```python
USE_CAMERA = True
CAMERA_INDEX = 0
```

Run

```bash
python main.py
```

---

### Using Video

In `config.py`

```python
USE_CAMERA = False
VIDEO_PATH = "people.mp4"
```

Run

```bash
python main.py
```

---

## 📁 Generated Outputs

After execution, the following files are generated inside the **Outputs** directory.

- 🎥 processed_video.mp4
- 📊 analytics_summary.csv
- 📄 analytics_summary.json

---

## 📈 Analytics Provided

- Current People Count
- Unique Visitors
- Entry Count
- Exit Count
- Peak Crowd
- Average Crowd
- Runtime Statistics
- Average FPS

---

## 📸 Screenshots

> Add screenshots of:
>
> - Person Detection
> - Live Dashboard
> - Heatmap
> - Output Video

---

## 🚀 Future Improvements

- DeepSORT / ByteTrack Integration
- Multi-Camera Support
- Face Recognition
- Person Re-identification
- Streamlit Dashboard
- Flask REST API
- Database Integration
- Cloud Deployment
- Docker Support
- Email Alert System

---

## 👨‍💻 Author

**Srinath Rajasekar R**

BE Computer Science and Engineering

GitHub: https://github.com/sri-13-pro

---

## 📄 License

This project is licensed under the MIT License.
