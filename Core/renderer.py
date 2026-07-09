"""
=========================================================
Smart People Flow Analytics Pro
Professional Rendering Engine
=========================================================
"""

import cv2
import math
import colorsys

from config import *


class Renderer:

    def __init__(self):

        self.font = cv2.FONT_HERSHEY_SIMPLEX

        self.font_scale = LABEL_FONT_SCALE

        self.font_thickness = LABEL_THICKNESS

    # =====================================================
    # Dynamic Color Generator
    # =====================================================

    def get_color(self, track_id):

        hue = ((track_id * 47) % 360) / 360

        r, g, b = colorsys.hsv_to_rgb(

            hue,

            0.85,

            1.0

        )

        return (

            int(b * 255),

            int(g * 255),

            int(r * 255)

        )

    # =====================================================
    # Rounded Rectangle
    # =====================================================

    def rounded_rectangle(

        self,

        frame,

        pt1,

        pt2,

        color,

        thickness=2,

        radius=10

    ):

        x1, y1 = pt1

        x2, y2 = pt2

        cv2.line(frame, (x1 + radius, y1), (x2 - radius, y1), color, thickness)

        cv2.line(frame, (x1 + radius, y2), (x2 - radius, y2), color, thickness)

        cv2.line(frame, (x1, y1 + radius), (x1, y2 - radius), color, thickness)

        cv2.line(frame, (x2, y1 + radius), (x2, y2 - radius), color, thickness)

        cv2.ellipse(frame, (x1 + radius, y1 + radius),

                    (radius, radius),

                    180,

                    0,

                    90,

                    color,

                    thickness)

        cv2.ellipse(frame, (x2 - radius, y1 + radius),

                    (radius, radius),

                    270,

                    0,

                    90,

                    color,

                    thickness)

        cv2.ellipse(frame, (x1 + radius, y2 - radius),

                    (radius, radius),

                    90,

                    0,

                    90,

                    color,

                    thickness)

        cv2.ellipse(frame, (x2 - radius, y2 - radius),

                    (radius, radius),

                    0,

                    0,

                    90,

                    color,

                    thickness)

    # =====================================================
    # Filled Rounded Rectangle
    # =====================================================

    def filled_box(

        self,

        frame,

        x,

        y,

        w,

        h,

        color

    ):

        overlay = frame.copy()

        cv2.rectangle(

            overlay,

            (x, y),

            (x + w, y + h),

            color,

            -1

        )

        cv2.addWeighted(

            overlay,

            0.90,

            frame,

            0.10,

            0,

            frame

        )

    # =====================================================
    # Crosshair
    # =====================================================

    def draw_crosshair(

        self,

        frame,

        center,

        color

    ):

        x, y = center

        size = 8

        cv2.line(

            frame,

            (x - size, y),

            (x + size, y),

            color,

            1

        )

        cv2.line(

            frame,

            (x, y - size),

            (x, y + size),

            color,

            1

        )

        cv2.circle(

            frame,

            (x, y),

            2,

            color,

            -1

        )

    # =====================================================
    # Feet Marker
    # =====================================================

    def draw_feet(

        self,

        frame,

        center,

        color

    ):

        x, y = center

        cv2.circle(

            frame,

            (x, y),

            8,

            color,

            2

        )

        cv2.circle(

            frame,

            (x, y),

            3,

            color,

            -1

        )

        self.draw_crosshair(

            frame,

            center,

            color

        )
            # =====================================================
    # Draw Person
    # =====================================================

    def draw_person(self, frame, detection):

        track_id = detection["id"]
        conf = detection["confidence"]

        x1, y1, x2, y2 = detection["bbox"]

        center = detection["center"]

        color = self.get_color(track_id)

        # -------------------------
        # Bounding Box
        # -------------------------

        if SHOW_BOUNDING_BOX:

            self.rounded_rectangle(

                frame,

                (x1, y1),

                (x2, y2),

                color,

                thickness=BOUNDING_BOX_THICKNESS

            )

        # -------------------------
        # Feet Marker
        # -------------------------

        if SHOW_CENTER_POINT:

            self.draw_feet(

                frame,

                center,

                color

            )

        # -------------------------
        # Label
        # -------------------------

        if SHOW_LABEL:

            self.draw_label(

                frame,

                x1,

                y1,

                track_id,

                conf,

                color

            )

    # =====================================================
    # Draw Label
    # =====================================================

    def draw_label(

        self,

        frame,

        x,

        y,

        track_id,

        confidence,

        color

    ):

        label = f"ID {track_id}"

        confidence_text = f"{confidence*100:.1f}%"

        (w1, h1), _ = cv2.getTextSize(

            label,

            self.font,

            self.font_scale,

            self.font_thickness

        )

        (w2, h2), _ = cv2.getTextSize(

            confidence_text,

            self.font,

            self.font_scale,

            self.font_thickness

        )

        width = max(w1, w2) + 18

        height = h1 + h2 + 24

        y = max(height + 5, y)

        self.filled_box(

            frame,

            x,

            y - height,

            width,

            height,

            color

        )

        cv2.putText(

            frame,

            label,

            (x + 8, y - height + 20),

            self.font,

            self.font_scale,

            WHITE,

            self.font_thickness

        )

        cv2.putText(

            frame,

            confidence_text,

            (x + 8, y - 8),

            self.font,

            self.font_scale,

            WHITE,

            self.font_thickness

        )

    # =====================================================
    # Draw Trajectory
    # =====================================================

    def draw_trajectory(

        self,

        frame,

        path,

        track_id

    ):

        if len(path) < 2:

            return

        color = self.get_color(track_id)

        for i in range(1, len(path)):

            thickness = max(

                1,

                min(5, i // 10)

            )

            cv2.line(

                frame,

                path[i - 1],

                path[i],

                color,

                thickness

            )

    # =====================================================
    # Entry / Exit Line
    # =====================================================

    def draw_entry_line(

        self,

        frame,

        line_x,

        height

    ):

        cv2.line(

            frame,

            (line_x, 0),

            (line_x, height),

            YELLOW,

            2

        )

        cv2.putText(

            frame,

            "ENTRY / EXIT",

            (line_x - 70, 30),

            self.font,

            0.6,

            YELLOW,

            2

        )

    # =====================================================
    # Draw FPS
    # =====================================================

    def draw_fps(

        self,

        frame,

        fps

    ):

        cv2.putText(

            frame,

            f"FPS : {fps:.1f}",

            (20, 35),

            self.font,

            0.7,

            GREEN,

            2

        )
            # =====================================================
    # Dashboard Panel
    # =====================================================

    def draw_dashboard(
        self,
        frame,
        stats
    ):

        if not SHOW_DASHBOARD:
            return

        panel_width = 320
        panel_height = 220

        x = 15
        y = 55

        overlay = frame.copy()

        cv2.rectangle(
            overlay,
            (x, y),
            (x + panel_width, y + panel_height),
            PANEL_COLOR,
            -1
        )

        cv2.addWeighted(
            overlay,
            0.65,
            frame,
            0.35,
            0,
            frame
        )

        cv2.rectangle(
            frame,
            (x, y),
            (x + panel_width, y + panel_height),
            CYAN,
            2
        )

        cv2.putText(
            frame,
            "SMART PEOPLE ANALYTICS",
            (x + 10, y + 28),
            self.font,
            0.65,
            WHITE,
            2
        )

        line_y = y + 60

        for key, value in stats.items():

            cv2.putText(
                frame,
                f"{key}",
                (x + 15, line_y),
                self.font,
                0.55,
                WHITE,
                2
            )

            cv2.putText(
                frame,
                str(value),
                (x + 220, line_y),
                self.font,
                0.60,
                CYAN,
                2
            )

            line_y += 28

    # =====================================================
    # Heatmap Legend
    # =====================================================

    def draw_heatmap_legend(
        self,
        frame
    ):

        h, w = frame.shape[:2]

        bar_height = 180
        bar_width = 20

        x = w - 55
        y = 60

        gradient = []

        for i in range(bar_height):

            value = int(
                255 * (1 - i / bar_height)
            )

            gradient.append(value)

        gradient = [[v] for v in gradient]

        import numpy as np

        gradient = np.array(
            gradient,
            dtype=np.uint8
        )

        gradient = cv2.applyColorMap(
            gradient,
            HEATMAP_COLORMAP
        )

        gradient = cv2.resize(
            gradient,
            (bar_width, bar_height)
        )

        frame[
            y:y + bar_height,
            x:x + bar_width
        ] = gradient

        cv2.rectangle(
            frame,
            (x, y),
            (x + bar_width, y + bar_height),
            WHITE,
            1
        )

        cv2.putText(
            frame,
            "HIGH",
            (x - 18, y - 8),
            self.font,
            0.45,
            WHITE,
            1
        )

        cv2.putText(
            frame,
            "LOW",
            (x - 12, y + bar_height + 18),
            self.font,
            0.45,
            WHITE,
            1
        )

    # =====================================================
    # Runtime
    # =====================================================

    def draw_runtime(
        self,
        frame,
        runtime_seconds
    ):

        hrs = int(runtime_seconds // 3600)
        mins = int((runtime_seconds % 3600) // 60)
        secs = int(runtime_seconds % 60)

        runtime = f"{hrs:02}:{mins:02}:{secs:02}"

        cv2.putText(
            frame,
            f"Runtime : {runtime}",
            (20, frame.shape[0] - 20),
            self.font,
            0.65,
            GREEN,
            2
        )

    # =====================================================
    # Draw Title
    # =====================================================

    def draw_title(
        self,
        frame,
        title="Smart People Flow Analytics Pro"
    ):

        cv2.putText(
            frame,
            title,
            (20, 25),
            self.font,
            0.75,
            CYAN,
            2
        )

    # =====================================================
    # Draw Frame Border
    # =====================================================

    def draw_border(
        self,
        frame
    ):

        h, w = frame.shape[:2]

        cv2.rectangle(
            frame,
            (3, 3),
            (w - 3, h - 3),
            CYAN,
            2
        )