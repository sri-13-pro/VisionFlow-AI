"""
=========================================================
Smart People Flow Analytics Pro
Main Application
=========================================================
"""

import os
import time
import cv2

from config import *

from core.detector import PeopleDetector
from core.tracker import PersonTracker
from core.renderer import Renderer
from core.heatmap import Heatmap
from core.zones import Zone, ZoneManager
from core.analytics import Analytics
from core.dashboard import Dashboard



# ==========================================================
# Initialize Modules
# ==========================================================

print("=" * 60)
print("SMART PEOPLE FLOW ANALYTICS PRO")
print("=" * 60)

detector = PeopleDetector()

tracker = PersonTracker()

renderer = Renderer()

heatmap = Heatmap()

analytics = Analytics()

dashboard = Dashboard()

zone_manager = ZoneManager()

print("✓ All modules initialized successfully")

# ==========================================================
# Create Zones
# ==========================================================

zone_manager.add_zone(

    Zone(

        "Entrance",

        [

            (40, 80),

            (350, 80),

            (350, 450),

            (40, 450)

        ],

        (0,255,0)

    )

)

zone_manager.add_zone(

    Zone(

        "Center",

        [

            (360,80),

            (820,80),

            (820,450),

            (360,450)

        ],

        (255,255,0)

    )

)

zone_manager.add_zone(

    Zone(

        "Exit",

        [

            (830,80),

            (1250,80),

            (1250,450),

            (830,450)

        ],

        (0,0,255)

    )

)

print("✓ Zones Created")

# ==========================================================
# Video Source
# ==========================================================
if USE_CAMERA:
    print("Using Webcam...")
    cap = cv2.VideoCapture(CAMERA_INDEX)
else:
    print(f"Using Video File: {VIDEO_PATH}")
    cap = cv2.VideoCapture(VIDEO_PATH)

if not cap.isOpened():
    raise RuntimeError("Unable to open camera or video source.")

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

# If FPS is not available, use a default
if fps <= 0:
    fps = 30

print(f"Resolution : {width}x{height}")
print(f"FPS : {fps}")

writer = cv2.VideoWriter(
    OUTPUT_VIDEO,
    cv2.VideoWriter_fourcc(*'mp4v'),
    fps,
    (width, height)
)

# ==========================================================
# Heatmap Initialization
# ==========================================================

ret, frame = cap.read()

if not ret:

    raise RuntimeError("Unable to read first frame.")

heatmap.initialize(frame)

cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

print("✓ Heatmap Initialized")

# ==========================================================
# Runtime
# ==========================================================

start_time = time.time()

frame_number = 0

print("\nStarting Processing...\n")
# ==========================================================
# Main Processing Loop
# ==========================================================

while True:

    ret, frame = cap.read()

    if not ret:
        break

    frame_number += 1

    # ------------------------------------------------------
    # Detection
    # ------------------------------------------------------

    detections = detector.detect(frame)

    # ------------------------------------------------------
    # Tracking + Heatmap
    # ------------------------------------------------------

    for detection in detections:

        track_id = detection["id"]

        center = detection["center"]

        tracker.update(
            track_id,
            center,
            ENTRY_LINE_X
        )

        heatmap.update(
            center=center,
            path=tracker.get_path(track_id)
        )

    # ------------------------------------------------------
    # Cleanup Old Tracks
    # ------------------------------------------------------

    tracker.cleanup()

    # ------------------------------------------------------
    # Zone Analytics
    # ------------------------------------------------------

    zone_manager.update(tracker)

    # ------------------------------------------------------
    # Analytics
    # ------------------------------------------------------

    analytics.update(
        tracker,
        detector,
        heatmap
    )

    # ------------------------------------------------------
    # Heatmap Overlay
    # ------------------------------------------------------

    if SHOW_HEATMAP:

        frame = heatmap.overlay(frame)

    # ------------------------------------------------------
    # Draw Zones
    # ------------------------------------------------------

    zone_manager.draw(frame)

    # ------------------------------------------------------
    # Draw People
    # ------------------------------------------------------

    for detection in detections:

        track_id = detection["id"]

        renderer.draw_person(
            frame,
            detection
        )

        renderer.draw_trajectory(
            frame,
            tracker.get_path(track_id),
            track_id
        )

    # ------------------------------------------------------
    # Entry / Exit Line
    # ------------------------------------------------------

    renderer.draw_entry_line(
        frame,
        ENTRY_LINE_X,
        height
    )

    # ------------------------------------------------------
    # Title
    # ------------------------------------------------------

    renderer.draw_title(
        frame
    )

    # ------------------------------------------------------
    # Border
    # ------------------------------------------------------

    renderer.draw_border(
        frame
    )

    # ------------------------------------------------------
    # Runtime
    # ------------------------------------------------------

    renderer.draw_runtime(
        frame,
        time.time() - start_time
    )

    # ------------------------------------------------------
    # FPS
    # ------------------------------------------------------

    renderer.draw_fps(
        frame,
        detector.inference_fps()
    )

    # ------------------------------------------------------
    # Dashboard
    # ------------------------------------------------------

    dashboard.render(
        frame,
        analytics,
        tracker,
        heatmap,
        zone_manager
    )
    cv2.namedWindow("Smart People Flow Analytics Pro", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Smart People Flow Analytics Pro", 1280, 720)
    cv2.imshow("Smart People Flow Analytics Pro", frame)
    

    # ------------------------------------------------------
    # Save Output Video
    # ------------------------------------------------------

    writer.write(frame)

    # ------------------------------------------------------
    # Keyboard Controls
    # ------------------------------------------------------

    key = cv2.waitKey(1) & 0xFF

    # Quit
    if key == ord('q'):

        print("\nStopping application...")
        break

    # Reset Heatmap
    elif key == ord('r'):

        heatmap.reset()

        print("✓ Heatmap Reset")

    # Save Snapshot
    elif key == ord('s'):

        snapshot_name = os.path.join(

            "outputs",

            f"snapshot_{frame_number}.jpg"

        )

        cv2.imwrite(

            snapshot_name,

            frame

        )

        print(f"✓ Snapshot Saved : {snapshot_name}")

    # Save Heatmap
    elif key == ord('h'):

        if heatmap.save():

            print("✓ Heatmap Saved")

    # Export Analytics
    elif key == ord('e'):

        csv_file = analytics.export_csv(

            tracker,

            heatmap,

            zone_manager

        )

        json_file = analytics.export_json(

            tracker,

            heatmap,

            zone_manager

        )

        print(f"✓ CSV Exported : {csv_file}")

        print(f"✓ JSON Exported : {json_file}")

    # ------------------------------------------------------
    # Console Status (Every 100 Frames)
    # ------------------------------------------------------

    if frame_number % 100 == 0:

        summary = analytics.summary(

            tracker,

            heatmap,

            zone_manager

        )

        print("\n" + "=" * 60)

        print(f"Frame : {frame_number}")

        print(f"People : {summary['Current People']}")

        print(f"Visitors : {summary['Unique Visitors']}")

        print(f"Entries : {summary['Entries']}")

        print(f"Exits : {summary['Exits']}")

        print(f"Density : {summary['Heat Density']}%")

        print(f"FPS : {summary['Average FPS']}")

        print("=" * 60)
        # ==========================================================
# Save Final Outputs
# ==========================================================

print("\nSaving final outputs...")

try:

    heatmap.save()

    print("✓ Heatmap saved.")

except Exception as e:

    print(f"Heatmap save failed: {e}")

try:

    analytics.export_csv(

        tracker,

        heatmap,

        zone_manager

    )

    analytics.export_json(

        tracker,

        heatmap,

        zone_manager

    )

    print("✓ Analytics exported.")

except Exception as e:

    print(f"Analytics export failed: {e}")

# ==========================================================
# Release Resources
# ==========================================================

cap.release()

writer.release()

cv2.destroyAllWindows()

# ==========================================================
# Final Summary
# ==========================================================

elapsed = time.time() - start_time

summary = analytics.summary(

    tracker,

    heatmap,

    zone_manager

)

print("\n" + "=" * 60)
print("SMART PEOPLE FLOW ANALYTICS PRO")
print("=" * 60)

print(f"Runtime           : {elapsed:.2f} sec")
print(f"Frames Processed  : {frame_number}")
print(f"Average FPS       : {analytics.average_fps():.2f}")

print(f"Current People    : {summary['Current People']}")
print(f"Unique Visitors   : {summary['Unique Visitors']}")
print(f"Entries           : {summary['Entries']}")
print(f"Exits             : {summary['Exits']}")

print(f"Peak Crowd        : {summary['Peak Crowd']}")
print(f"Average Crowd     : {summary['Average Crowd']}")

print(f"Heat Density      : {summary['Heat Density']}%")
print(f"Maximum Heat      : {summary['Maximum Heat']}")

print("=" * 60)
print("Application Closed Successfully.")
print("=" * 60)