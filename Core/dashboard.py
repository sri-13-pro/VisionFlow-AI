"""
=========================================================
Smart People Flow Analytics Pro
Professional Dashboard
=========================================================
"""

import cv2
import numpy as np


class Dashboard:

    def __init__(self):

        self.width = 340

        self.margin = 15

        self.font = cv2.FONT_HERSHEY_SIMPLEX

    # =====================================================
    # Transparent Panel
    # =====================================================

    def panel(

        self,

        frame,

        x,

        y,

        w,

        h,

        alpha=0.65

    ):

        overlay = frame.copy()

        cv2.rectangle(

            overlay,

            (x, y),

            (x + w, y + h),

            (30, 30, 30),

            -1

        )

        cv2.addWeighted(

            overlay,

            alpha,

            frame,

            1 - alpha,

            0,

            frame

        )

        cv2.rectangle(

            frame,

            (x, y),

            (x + w, y + h),

            (0, 255, 255),

            2

        )

    # =====================================================
    # KPI Card
    # =====================================================

    def card(

        self,

        frame,

        x,

        y,

        title,

        value,

        color=(0,255,255)

    ):

        cv2.rectangle(

            frame,

            (x,y),

            (x+145,y+65),

            (45,45,45),

            -1

        )

        cv2.rectangle(

            frame,

            (x,y),

            (x+145,y+65),

            color,

            2

        )

        cv2.putText(

            frame,

            title,

            (x+10,y+22),

            self.font,

            0.5,

            (255,255,255),

            1

        )

        cv2.putText(

            frame,

            str(value),

            (x+10,y+52),

            self.font,

            0.9,

            color,

            2

        )

    # =====================================================
    # Section Title
    # =====================================================

    def title(

        self,

        frame,

        text,

        x,

        y

    ):

        cv2.putText(

            frame,

            text,

            (x,y),

            self.font,

            0.65,

            (255,255,255),

            2

        )
            # =====================================================
    # Draw Dashboard
    # =====================================================

    def draw(
        self,
        frame,
        analytics,
        tracker,
        heatmap,
        zone_manager
    ):

        panel_x = 15
        panel_y = 60
        panel_w = self.width
        panel_h = 420

        self.panel(
            frame,
            panel_x,
            panel_y,
            panel_w,
            panel_h
        )

        self.title(
            frame,
            "SMART ANALYTICS",
            panel_x + 15,
            panel_y + 30
        )

        # ----------------------------------------
        # KPI Cards
        # ----------------------------------------

        crowd = analytics.crowd_statistics(tracker)

        self.card(
            frame,
            panel_x + 15,
            panel_y + 45,
            "People",
            crowd["Current People"],
            (0,255,255)
        )

        self.card(
            frame,
            panel_x + 175,
            panel_y + 45,
            "Visitors",
            crowd["Unique Visitors"],
            (0,255,0)
        )

        self.card(
            frame,
            panel_x + 15,
            panel_y + 125,
            "Entries",
            crowd["Entries"],
            (255,255,0)
        )

        self.card(
            frame,
            panel_x + 175,
            panel_y + 125,
            "Exits",
            crowd["Exits"],
            (0,128,255)
        )

        # ----------------------------------------
        # Runtime & FPS
        # ----------------------------------------

        cv2.putText(
            frame,
            f"Runtime : {analytics.format_runtime()}",
            (panel_x + 15, panel_y + 225),
            self.font,
            0.55,
            (255,255,255),
            2
        )

        cv2.putText(
            frame,
            f"FPS : {analytics.average_fps():.1f}",
            (panel_x + 15, panel_y + 250),
            self.font,
            0.55,
            (0,255,0),
            2
        )

        cv2.putText(
            frame,
            f"Density : {heatmap.density():.2f}%",
            (panel_x + 15, panel_y + 275),
            self.font,
            0.55,
            (0,255,255),
            2
        )

        cv2.putText(
            frame,
            f"Peak Crowd : {analytics.peak_people}",
            (panel_x + 15, panel_y + 300),
            self.font,
            0.55,
            (255,255,255),
            2
        )

        # ----------------------------------------
        # Zone Statistics
        # ----------------------------------------

        cv2.putText(
            frame,
            "Zones",
            (panel_x + 15, panel_y + 335),
            self.font,
            0.60,
            (255,255,255),
            2
        )

        y = panel_y + 360

        for zone in zone_manager:

            text = f"{zone.name}: {zone.count()}"

            cv2.putText(
                frame,
                text,
                (panel_x + 20, y),
                self.font,
                0.50,
                zone.color,
                2
            )

            y += 25
                # =====================================================
    # Mini Trend Graph
    # =====================================================

    def draw_people_graph(
        self,
        frame,
        analytics,
        x,
        y,
        width=300,
        height=80
    ):

        history = analytics.history()["People"]

        if len(history) < 2:
            return

        cv2.rectangle(
            frame,
            (x, y),
            (x + width, y + height),
            (70, 70, 70),
            1
        )

        max_people = max(history)

        if max_people == 0:
            max_people = 1

        points = []

        step = max(1, len(history) // width)

        values = history[::step]

        for i, value in enumerate(values):

            px = x + int(i * width / max(len(values) - 1, 1))

            py = y + height - int((value / max_people) * height)

            points.append((px, py))

        for i in range(1, len(points)):

            cv2.line(
                frame,
                points[i - 1],
                points[i],
                (0, 255, 255),
                2
            )

        cv2.putText(
            frame,
            "People Trend",
            (x, y - 8),
            self.font,
            0.5,
            (255, 255, 255),
            1
        )

    # =====================================================
    # Status Indicator
    # =====================================================

    def draw_status(
        self,
        frame,
        online=True
    ):

        color = (0, 255, 0) if online else (0, 0, 255)

        text = "SYSTEM ONLINE" if online else "SYSTEM OFFLINE"

        cv2.circle(
            frame,
            (25, frame.shape[0] - 25),
            8,
            color,
            -1
        )

        cv2.putText(
            frame,
            text,
            (40, frame.shape[0] - 18),
            self.font,
            0.55,
            color,
            2
        )

    # =====================================================
    # Footer
    # =====================================================

    def draw_footer(
        self,
        frame
    ):

        text = "Smart People Flow Analytics Pro | AI Vision Dashboard"

        size = cv2.getTextSize(
            text,
            self.font,
            0.45,
            1
        )[0]

        x = frame.shape[1] - size[0] - 15

        y = frame.shape[0] - 18

        cv2.putText(
            frame,
            text,
            (x, y),
            self.font,
            0.45,
            (180, 180, 180),
            1
        )

    # =====================================================
    # Complete Dashboard
    # =====================================================

    def render(
        self,
        frame,
        analytics,
        tracker,
        heatmap,
        zone_manager
    ):

        self.draw(
            frame,
            analytics,
            tracker,
            heatmap,
            zone_manager
        )

        self.draw_people_graph(
            frame,
            analytics,
            20,
            500
        )

        self.draw_status(
            frame,
            True
        )

        self.draw_footer(
            frame
        )