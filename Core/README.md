# Core Modules

This directory contains the core components of the **VisionFlow AI** system. Each module is designed with a modular architecture, making the project easier to maintain, extend, and debug.

---

## Module Overview

### `detector.py`
Responsible for detecting people in video frames using the **YOLOv8** object detection model.

**Responsibilities**
- Load the YOLO model
- Detect people in each frame
- Filter detections by confidence
- Return bounding boxes and detection scores

---

### `tracker.py`
Tracks detected people across consecutive frames.

**Responsibilities**
- Assign unique IDs to detected people
- Maintain object identity
- Reduce duplicate detections
- Track movement paths

---

### `analytics.py`
Calculates real-time crowd statistics.

**Responsibilities**
- Current people count
- Unique visitor count
- Entry and exit counting
- Peak crowd calculation
- Average crowd calculation
- Runtime statistics
- Export analytics reports

---

### `heatmap.py`
Generates a movement heatmap based on tracked person locations.

**Responsibilities**
- Record movement positions
- Update heat intensity
- Normalize heat values
- Generate colored heatmaps
- Save final heatmap image

---

### `zones.py`
Defines and manages monitoring zones.

**Responsibilities**
- Create virtual zones
- Check whether people enter or leave zones
- Support entry/exit analysis

---

### `renderer.py`
Handles all visual overlays displayed on video frames.

**Responsibilities**
- Draw bounding boxes
- Draw tracking IDs
- Render heatmaps
- Display analytics
- Draw zones
- Show FPS and statistics

---

### `dashboard.py`
Displays real-time analytics information.

**Responsibilities**
- Live people count
- Visitor count
- Entry/Exit statistics
- Crowd density
- Peak crowd
- FPS monitoring

---

## Architecture

```
Video/Webcam
      │
      ▼
 detector.py
      │
      ▼
 tracker.py
      │
      ▼
 zones.py
      │
      ▼
 analytics.py
      │
      ▼
 heatmap.py
      │
      ▼
 renderer.py
      │
      ▼
 dashboard.py
      │
      ▼
 Output Video & Reports
```

---

## Design Principles

- Modular architecture
- High code readability
- Reusable components
- Easy debugging
- Scalable design
- Separation of concerns

---

## Dependencies

The core modules rely on:

- Python
- OpenCV
- Ultralytics YOLOv8
- NumPy
- Pandas
- Matplotlib

---

## Future Enhancements

- DeepSORT integration
- ByteTrack optimization
- Multi-camera tracking
- Person re-identification
- Face recognition
- Cloud analytics
- REST API support
- Database integration
