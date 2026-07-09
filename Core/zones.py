"""
=========================================================
Smart People Flow Analytics Pro
Zone Management System
=========================================================
"""

import cv2
import numpy as np
import time


class Zone:

    def __init__(
        self,
        name,
        points,
        color=(0, 255, 0)
    ):

        self.name = name

        self.points = np.array(
            points,
            dtype=np.int32
        )

        self.color = color

        self.current_people = set()

        self.total_entries = 0

        self.total_exits = 0

        self.max_occupancy = 0

        self.created_time = time.time()

    # =====================================================
    # Check if Point is Inside Zone
    # =====================================================

    def contains(self, point):

        x, y = point

        result = cv2.pointPolygonTest(
            self.points,
            (int(x), int(y)),
            False
        )

        return result >= 0

    # =====================================================
    # Update Occupancy
    # =====================================================

    def update_people(self, people_ids):

        previous = self.current_people.copy()

        current = set(people_ids)

        entered = current - previous

        exited = previous - current

        self.total_entries += len(entered)

        self.total_exits += len(exited)

        self.current_people = current

        self.max_occupancy = max(
            self.max_occupancy,
            len(current)
        )

    # =====================================================
    # Current Count
    # =====================================================

    def count(self):

        return len(self.current_people)

    # =====================================================
    # Statistics
    # =====================================================

    def statistics(self):

        return {

            "Zone": self.name,

            "Current": self.count(),

            "Entries": self.total_entries,

            "Exits": self.total_exits,

            "Peak": self.max_occupancy

        }
    # ==========================================================
# Zone Manager
# ==========================================================

class ZoneManager:

    def __init__(self):

        self.zones = []

    # =====================================================
    # Add Zone
    # =====================================================

    def add_zone(self, zone):

        self.zones.append(zone)

    # =====================================================
    # Remove Zone
    # =====================================================

    def remove_zone(self, zone_name):

        self.zones = [

            zone for zone in self.zones

            if zone.name != zone_name

        ]

    # =====================================================
    # Clear Zones
    # =====================================================

    def clear(self):

        self.zones.clear()

    # =====================================================
    # Find Zone
    # =====================================================

    def find_zone(self, point):

        for zone in self.zones:

            if zone.contains(point):

                return zone.name

        return "Outside"

    # =====================================================
    # Update Zones
    # =====================================================

    def update(self, tracker):

        """
        Update all zones based on current tracker state.
        """

        zone_people = {

            zone.name: []

            for zone in self.zones

        }

        for person in tracker:

            zone_name = self.find_zone(

                person.current_position

            )

            person.update_zone(zone_name)

            if zone_name != "Outside":

                zone_people[zone_name].append(

                    person.id

                )

        for zone in self.zones:

            zone.update_people(

                zone_people[zone.name]

            )

    # =====================================================
    # Get Zone Object
    # =====================================================

    def get_zone(self, name):

        for zone in self.zones:

            if zone.name == name:

                return zone

        return None

    # =====================================================
    # Statistics
    # =====================================================

    def statistics(self):

        return [

            zone.statistics()

            for zone in self.zones

        ]
        # =====================================================
    # Draw Zones
    # =====================================================

    def draw(self, frame):

        for zone in self.zones:

            # Draw polygon
            cv2.polylines(
                frame,
                [zone.points],
                True,
                zone.color,
                2
            )

            # Semi-transparent fill
            overlay = frame.copy()

            cv2.fillPoly(
                overlay,
                [zone.points],
                zone.color
            )

            cv2.addWeighted(
                overlay,
                0.15,
                frame,
                0.85,
                0,
                frame
            )

            # Zone Center
            center = self.get_center(zone.points)

            # Zone Name
            cv2.putText(
                frame,
                zone.name,
                (center[0] - 40, center[1] - 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.65,
                (255, 255, 255),
                2
            )

            # Occupancy
            cv2.putText(
                frame,
                f"People : {zone.count()}",
                (center[0] - 50, center[1] + 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                zone.color,
                2
            )

            # Peak Occupancy
            cv2.putText(
                frame,
                f"Peak : {zone.max_occupancy}",
                (center[0] - 40, center[1] + 28),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.50,
                (255, 255, 255),
                1
            )

    # =====================================================
    # Polygon Center
    # =====================================================

    def get_center(self, points):

        moments = cv2.moments(points)

        if moments["m00"] == 0:

            return tuple(points[0])

        cx = int(moments["m10"] / moments["m00"])

        cy = int(moments["m01"] / moments["m00"])

        return (cx, cy)

    # =====================================================
    # Number of Zones
    # =====================================================

    def __len__(self):

        return len(self.zones)

    # =====================================================
    # Iterator
    # =====================================================

    def __iter__(self):

        return iter(self.zones)

    # =====================================================
    # Zone Names
    # =====================================================

    def names(self):

        return [

            zone.name

            for zone in self.zones

        ]

    # =====================================================
    # Reset Statistics
    # =====================================================

    def reset(self):

        for zone in self.zones:

            zone.current_people.clear()

            zone.total_entries = 0

            zone.total_exits = 0

            zone.max_occupancy = 0

    # =====================================================
    # Print Statistics
    # =====================================================

    def print_statistics(self):

        print("\n" + "=" * 60)

        print("ZONE STATISTICS")

        print("=" * 60)

        for zone in self.zones:

            print(

                f"{zone.name:15}"

                f" Current:{zone.count():3}"

                f"  Entries:{zone.total_entries:3}"

                f"  Exits:{zone.total_exits:3}"

                f"  Peak:{zone.max_occupancy:3}"

            )

        print("=" * 60)