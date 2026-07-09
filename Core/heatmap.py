"""
=========================================================
Smart People Flow Analytics Pro
Heatmap Engine
=========================================================
"""

import cv2
import numpy as np

from config import (
    HEAT_RADIUS,
    HEAT_INTENSITY,
    HEAT_ALPHA,
    HEAT_DECAY,
    HEATMAP_COLORMAP,
    OUTPUT_HEATMAP
)


class Heatmap:

    def __init__(self):

        self.heatmap = None

        self.height = None

        self.width = None

    # =====================================================
    # Initialize Heatmap
    # =====================================================

    def initialize(self, frame):

        self.height, self.width = frame.shape[:2]

        self.heatmap = np.zeros(
            (self.height, self.width),
            dtype=np.float32
        )

    # =====================================================
    # Check Initialization
    # =====================================================

    def is_initialized(self):

        return self.heatmap is not None

    # =====================================================
    # Reset Heatmap
    # =====================================================

    def reset(self):

        if self.heatmap is not None:

            self.heatmap.fill(0)

    # =====================================================
    # Add Heat at One Point
    # =====================================================

    def add_point(

        self,

        center,

        radius=HEAT_RADIUS,

        intensity=HEAT_INTENSITY

    ):

        if self.heatmap is None:

            return

        x, y = center

        cv2.circle(

            self.heatmap,

            (int(x), int(y)),

            radius,

            intensity,

            -1

        )

    # =====================================================
    # Add Multiple Points
    # =====================================================

    def add_points(

        self,

        points

    ):

        for point in points:

            self.add_point(point)

    # =====================================================
    # Apply Decay
    # =====================================================

    def decay(self):

        if self.heatmap is None:

            return

        self.heatmap *= HEAT_DECAY

    # =====================================================
    # Maximum Heat
    # =====================================================

    def max_heat(self):

        if self.heatmap is None:

            return 0

        return float(np.max(self.heatmap))

    # =====================================================
    # Average Heat
    # =====================================================

    def average_heat(self):

        if self.heatmap is None:

            return 0

        return float(np.mean(self.heatmap))
        # =====================================================
    # Add Trajectory Heat
    # =====================================================

    def add_path(
        self,
        path,
        intensity=1.0
    ):
        """
        Add heat along an entire trajectory.
        """

        if self.heatmap is None:
            return

        if len(path) < 2:
            return

        for i in range(1, len(path)):

            thickness = max(
                4,
                HEAT_RADIUS // 3
            )

            cv2.line(
                self.heatmap,
                path[i - 1],
                path[i],
                intensity,
                thickness
            )

            cv2.circle(
                self.heatmap,
                path[i],
                HEAT_RADIUS // 2,
                intensity,
                -1
            )

    # =====================================================
    # Gaussian Blur
    # =====================================================

    def smooth(self):

        if self.heatmap is None:
            return None

        return cv2.GaussianBlur(
            self.heatmap,
            (0, 0),
            sigmaX=18,
            sigmaY=18
        )

    # =====================================================
    # Normalize Heatmap
    # =====================================================

    def normalize(self):

        if self.heatmap is None:
            return None

        smooth_heat = self.smooth()

        normalized = cv2.normalize(
            smooth_heat,
            None,
            0,
            255,
            cv2.NORM_MINMAX
        )

        return normalized.astype(np.uint8)

    # =====================================================
    # Color Heatmap
    # =====================================================

    def colorize(self):

        normalized = self.normalize()

        if normalized is None:
            return None

        return cv2.applyColorMap(
            normalized,
            HEATMAP_COLORMAP
        )

    # =====================================================
    # Overlay Heatmap
    # =====================================================

    def overlay(
        self,
        frame
    ):

        colored = self.colorize()

        if colored is None:
            return frame

        return cv2.addWeighted(
            frame,
            1.0 - HEAT_ALPHA,
            colored,
            HEAT_ALPHA,
            0
        )

    # =====================================================
    # Density Score
    # =====================================================

    def density(self):

        if self.heatmap is None:
            return 0

        threshold = np.sum(
            self.heatmap > 5
        )

        total = self.height * self.width

        return round(
            (threshold / total) * 100,
            2
        )

    # =====================================================
    # Peak Heat
    # =====================================================

    def peak_location(self):

        if self.heatmap is None:
            return None

        _, _, _, max_loc = cv2.minMaxLoc(
            self.heatmap
        )

        return max_loc
        # =====================================================
    # Save Heatmap
    # =====================================================

    def save(self, filename=OUTPUT_HEATMAP):
        """
        Save the final heatmap image.
        """

        colored = self.colorize()

        if colored is None:
            return False

        cv2.imwrite(filename, colored)

        return True

    # =====================================================
    # Update Heatmap
    # =====================================================

    def update(
        self,
        center=None,
        path=None
    ):
        """
        One-step heatmap update.
        """

        if center is not None:
            self.add_point(center)

        if path is not None:
            self.add_path(path)

        self.decay()

    # =====================================================
    # Heat Statistics
    # =====================================================

    def statistics(self):

        if self.heatmap is None:

            return {
                "Maximum Heat": 0,
                "Average Heat": 0,
                "Density (%)": 0,
                "Peak Location": (0, 0)
            }

        return {

            "Maximum Heat": round(
                self.max_heat(),
                2
            ),

            "Average Heat": round(
                self.average_heat(),
                2
            ),

            "Density (%)": self.density(),

            "Peak Location": self.peak_location()

        }

    # =====================================================
    # Current Heatmap Image
    # =====================================================

    def image(self):

        return self.colorize()

    # =====================================================
    # Raw Heatmap
    # =====================================================

    def raw(self):

        return self.heatmap

    # =====================================================
    # Resize Heatmap
    # =====================================================

    def resize(
        self,
        width,
        height
    ):

        if self.heatmap is None:
            return

        self.heatmap = cv2.resize(
            self.heatmap,
            (width, height)
        )

        self.width = width
        self.height = height

    # =====================================================
    # Export Heatmap Array
    # =====================================================

    def export_array(self):

        if self.heatmap is None:
            return None

        return self.heatmap.copy()

    # =====================================================
    # Import Heatmap Array
    # =====================================================

    def import_array(
        self,
        array
    ):

        self.heatmap = array.copy()

        self.height, self.width = array.shape

    # =====================================================
    # Clear Heatmap
    # =====================================================

    def clear(self):

        self.reset()

    # =====================================================
    # String Representation
    # =====================================================

    def __str__(self):

        return (
            f"Heatmap("
            f"{self.width}x{self.height}, "
            f"Max={self.max_heat():.2f}, "
            f"Density={self.density():.2f}%"
            f")"
        )