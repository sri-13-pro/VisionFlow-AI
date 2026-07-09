"""
=========================================================
Smart People Flow Analytics Pro
Configuration File
=========================================================
"""

import os
import cv2

# =========================================================
# Project Information
# =========================================================

PROJECT_NAME = "Smart People Flow Analytics Pro"
VERSION = "1.0.0"

# =========================================================
# Paths
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ASSETS_DIR = os.path.join(BASE_DIR, "assets")
OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")

VIDEO_PATH = os.path.join(ASSETS_DIR, "people.mp4")
MODEL_PATH = "yolo11n.pt"

OUTPUT_VIDEO = os.path.join(OUTPUTS_DIR, "processed_video.mp4")
OUTPUT_HEATMAP = os.path.join(OUTPUTS_DIR, "heatmap.png")
OUTPUT_CSV = os.path.join(OUTPUTS_DIR, "analytics.csv")
OUTPUT_REPORT = os.path.join(OUTPUTS_DIR, "report.pdf")

# Create output directory automatically
os.makedirs(OUTPUTS_DIR, exist_ok=True)

# =========================================================
# Video Source
# =========================================================
USE_CAMERA = False
CAMERA_INDEX = 0
VIDEO_PATH = "assets/people.mp4"
# =========================================================
# Detection Settings
# =========================================================

CONFIDENCE_THRESHOLD = 0.35
IOU_THRESHOLD = 0.50

PERSON_CLASS_ID = 0

# =========================================================
# Tracking Settings
# =========================================================

TRACKER = "bytetrack"

TRACKER_CONFIG = "bytetrack.yaml"

MAX_HISTORY = 60

REMOVE_AFTER = 40

# =========================================================
# Heatmap Settings
# =========================================================

SHOW_HEATMAP = True

HEAT_RADIUS = 35

HEAT_INTENSITY = 2.0

HEAT_ALPHA = 0.45

HEAT_DECAY = 0.995

NORMALIZATION_PERCENTILE = 99

USE_TRAJECTORY_HEAT = True

HEATMAP_COLORMAP = cv2.COLORMAP_JET

# =========================================================
# Dashboard Settings
# =========================================================

SHOW_DASHBOARD = True

SHOW_FPS = True

SHOW_RUNTIME = True

SHOW_PEOPLE_COUNT = True

SHOW_PEAK_COUNT = True

SHOW_VISITORS = True

SHOW_ENTRY_EXIT = True

# =========================================================
# Rendering Settings
# =========================================================

SHOW_BOUNDING_BOX = True

SHOW_LABEL = True

SHOW_CENTER_POINT = True

SHOW_TRAJECTORY = True

BOUNDING_BOX_THICKNESS = 2

LABEL_FONT_SCALE = 0.55

LABEL_THICKNESS = 2

DISPLAY_SCALE = 1.0

# =========================================================
# Zone Settings
# =========================================================

ENABLE_ZONES = True

SHOW_ZONE_NAMES = True

SHOW_ZONE_OCCUPANCY = True

# =========================================================
# Entry / Exit Line
# =========================================================

SHOW_ENTRY_LINE = True

ENTRY_LINE_THICKNESS = 2

ENTRY_LINE_COLOR = (0, 255, 255)
# ==========================================
# Entry / Exit Line
# ==========================================

ENTRY_LINE_X = 424      # Middle of 848px video

ENTRY_LINE_COLOR = (0, 255, 255)

ENTRY_LINE_THICKNESS = 2

# =========================================================
# Performance
# =========================================================

SKIP_FRAMES = 0

ENABLE_GPU = False

# =========================================================
# Save Options
# =========================================================

SAVE_OUTPUT_VIDEO = True

SAVE_HEATMAP = True

CREATE_CSV = True

CREATE_PDF = False

# =========================================================
# Keyboard Shortcuts
# =========================================================

EXIT_KEY = 27      # ESC

PAUSE_KEY = ord("p")

RESET_HEATMAP_KEY = ord("r")

SCREENSHOT_KEY = ord("s")

# =========================================================
# Colors (BGR)
# =========================================================

WHITE = (255, 255, 255)

BLACK = (0, 0, 0)

RED = (0, 0, 255)

GREEN = (0, 255, 0)

BLUE = (255, 0, 0)

CYAN = (255, 255, 0)

YELLOW = (0, 255, 255)

ORANGE = (0, 165, 255)

PURPLE = (255, 0, 255)

GRAY = (150, 150, 150)

DARK_GRAY = (40, 40, 40)

LIGHT_GREEN = (80, 255, 80)

# =========================================================
# Dashboard Colors
# =========================================================

PANEL_COLOR = (30, 30, 30)

TEXT_COLOR = WHITE

VALUE_COLOR = CYAN

SUCCESS_COLOR = GREEN

WARNING_COLOR = ORANGE

DANGER_COLOR = RED

# =========================================================
# Logging
# =========================================================

ENABLE_LOGGING = True

LOG_LEVEL = "INFO"

# =========================================================
# End
# =========================================================