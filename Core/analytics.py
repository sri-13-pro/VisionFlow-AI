"""
=========================================================
Smart People Flow Analytics Pro
Enterprise Analytics Engine
=========================================================
"""

import time
from collections import deque
import numpy as np


class Analytics:

    def __init__(self):

        # ----------------------------------------
        # Session
        # ----------------------------------------

        self.start_time = time.time()

        self.frame_count = 0

        # ----------------------------------------
        # Crowd History
        # ----------------------------------------

        self.people_history = deque(maxlen=5000)

        self.entry_history = deque(maxlen=5000)

        self.exit_history = deque(maxlen=5000)

        self.fps_history = deque(maxlen=5000)

        # ----------------------------------------
        # Movement History
        # ----------------------------------------

        self.speed_history = deque(maxlen=5000)

        self.distance_history = deque(maxlen=5000)

        self.dwell_history = deque(maxlen=5000)

        # ----------------------------------------
        # Heatmap History
        # ----------------------------------------

        self.density_history = deque(maxlen=5000)

        self.max_heat_history = deque(maxlen=5000)

        # ----------------------------------------
        # Statistics
        # ----------------------------------------

        self.peak_people = 0

        self.average_people = 0

        self.total_distance = 0

        self.average_speed = 0

        self.average_dwell = 0

    # =====================================================
    # Update Analytics
    # =====================================================

    def update(

        self,

        tracker,

        detector,

        heatmap

    ):

        self.frame_count += 1

        current_people = tracker.current_people()

        self.people_history.append(

            current_people

        )

        self.entry_history.append(

            tracker.entry_count

        )

        self.exit_history.append(

            tracker.exit_count

        )

        self.fps_history.append(

            detector.inference_fps()

        )

        self.density_history.append(

            heatmap.density()

        )

        self.max_heat_history.append(

            heatmap.max_heat()

        )

        self.calculate_people()

        self.calculate_movement(

            tracker

        )

    # =====================================================
    # Crowd Statistics
    # =====================================================

    def calculate_people(self):

        if len(self.people_history) == 0:

            return

        self.peak_people = max(

            self.people_history

        )

        self.average_people = float(

            np.mean(

                self.people_history

            )

        )

    # =====================================================
    # Movement Statistics
    # =====================================================

    def calculate_movement(

        self,

        tracker

    ):

        speeds = []

        distances = []

        dwells = []

        for person in tracker:

            speeds.append(

                person.current_speed

            )

            distances.append(

                person.total_distance

            )

            dwells.append(

                person.dwell_time()

            )

        if len(speeds):

            self.average_speed = float(

                np.mean(

                    speeds

                )

            )

        if len(distances):

            self.total_distance = float(

                np.sum(

                    distances

                )

            )

        if len(dwells):

            self.average_dwell = float(

                np.mean(

                    dwells

                )

            )
                # =====================================================
    # Runtime
    # =====================================================

    def runtime(self):

        return time.time() - self.start_time

    # =====================================================
    # Current FPS
    # =====================================================

    def average_fps(self):

        if len(self.fps_history) == 0:
            return 0

        return float(np.mean(self.fps_history))

    # =====================================================
    # Heat Statistics
    # =====================================================

    def heat_statistics(self, heatmap):

        return {

            "Density (%)": round(
                heatmap.density(),
                2
            ),

            "Maximum Heat": round(
                heatmap.max_heat(),
                2
            ),

            "Average Heat": round(
                heatmap.average_heat(),
                2
            ),

            "Peak Location": heatmap.peak_location()

        }

    # =====================================================
    # Crowd Statistics
    # =====================================================

    def crowd_statistics(self, tracker):

        return {

            "Current People": tracker.current_people(),

            "Unique Visitors": tracker.total_visitors(),

            "Entries": tracker.entry_count,

            "Exits": tracker.exit_count,

            "Peak Crowd": self.peak_people,

            "Average Crowd": round(
                self.average_people,
                2
            )

        }

    # =====================================================
    # Movement Statistics
    # =====================================================

    def movement_statistics(self):

        return {

            "Average Speed": round(
                self.average_speed,
                2
            ),

            "Total Distance": round(
                self.total_distance,
                2
            ),

            "Average Dwell": round(
                self.average_dwell,
                2
            )

        }

    # =====================================================
    # Zone Statistics
    # =====================================================

    def zone_statistics(self, zone_manager):

        return zone_manager.statistics()

    # =====================================================
    # Dashboard Data
    # =====================================================

    def dashboard_data(
        self,
        tracker,
        heatmap
    ):

        return {

            "People": tracker.current_people(),

            "Visitors": tracker.total_visitors(),

            "Entries": tracker.entry_count,

            "Exits": tracker.exit_count,

            "Density": f"{heatmap.density():.2f}%",

            "FPS": f"{self.average_fps():.1f}",

            "Runtime": self.format_runtime()

        }

    # =====================================================
    # Runtime Formatter
    # =====================================================

    def format_runtime(self):

        seconds = int(self.runtime())

        hrs = seconds // 3600

        mins = (seconds % 3600) // 60

        secs = seconds % 60

        return f"{hrs:02}:{mins:02}:{secs:02}"

    # =====================================================
    # History
    # =====================================================

    def history(self):

        return {

            "People": list(self.people_history),

            "FPS": list(self.fps_history),

            "Density": list(self.density_history),

            "Entries": list(self.entry_history),

            "Exits": list(self.exit_history)

        }
        # =====================================================
    # Export Summary
    # =====================================================

    def summary(
        self,
        tracker,
        heatmap,
        zone_manager
    ):

        return {

            "Runtime": self.format_runtime(),

            "Frames Processed": self.frame_count,

            "Average FPS": round(
                self.average_fps(),
                2
            ),

            "Current People": tracker.current_people(),

            "Unique Visitors": tracker.total_visitors(),

            "Entries": tracker.entry_count,

            "Exits": tracker.exit_count,

            "Peak Crowd": self.peak_people,

            "Average Crowd": round(
                self.average_people,
                2
            ),

            "Average Speed": round(
                self.average_speed,
                2
            ),

            "Total Distance": round(
                self.total_distance,
                2
            ),

            "Average Dwell": round(
                self.average_dwell,
                2
            ),

            "Heat Density": round(
                heatmap.density(),
                2
            ),

            "Maximum Heat": round(
                heatmap.max_heat(),
                2
            ),

            "Zones": zone_manager.statistics()

        }

    # =====================================================
    # Export CSV
    # =====================================================

    def export_csv(
        self,
        tracker,
        heatmap,
        zone_manager,
        filename="outputs/analytics_summary.csv"
    ):

        import csv

        summary = self.summary(
            tracker,
            heatmap,
            zone_manager
        )

        with open(
            filename,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            writer.writerow(["Metric", "Value"])

            for key, value in summary.items():

                if key == "Zones":
                    continue

                writer.writerow([key, value])

            writer.writerow([])

            writer.writerow(["Zone", "Current", "Entries", "Exits", "Peak"])

            for zone in summary["Zones"]:

                writer.writerow([
                    zone["Zone"],
                    zone["Current"],
                    zone["Entries"],
                    zone["Exits"],
                    zone["Peak"]
                ])

        return filename

    # =====================================================
    # Export JSON
    # =====================================================

    def export_json(
        self,
        tracker,
        heatmap,
        zone_manager,
        filename="outputs/analytics_summary.json"
    ):

        import json

        summary = self.summary(
            tracker,
            heatmap,
            zone_manager
        )

        with open(
            filename,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                summary,
                file,
                indent=4
            )

        return filename

    # =====================================================
    # Reset Analytics
    # =====================================================

    def reset(self):

        self.start_time = time.time()

        self.frame_count = 0

        self.people_history.clear()
        self.entry_history.clear()
        self.exit_history.clear()
        self.fps_history.clear()

        self.speed_history.clear()
        self.distance_history.clear()
        self.dwell_history.clear()

        self.density_history.clear()
        self.max_heat_history.clear()

        self.peak_people = 0
        self.average_people = 0
        self.total_distance = 0
        self.average_speed = 0
        self.average_dwell = 0

    # =====================================================
    # String Representation
    # =====================================================

    def __str__(self):

        return (

            f"Analytics("

            f"Frames={self.frame_count}, "

            f"Peak={self.peak_people}, "

            f"Average FPS={self.average_fps():.2f}"

            f")"

        )