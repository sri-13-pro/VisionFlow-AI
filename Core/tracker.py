"""
=========================================================
Smart People Flow Analytics Pro
Enterprise Tracking Engine
=========================================================
"""

import math
import time
from collections import deque


class Person:

    def __init__(self, person_id, center):

        self.id = person_id

        # -------------------------
        # Position
        # -------------------------

        self.current_position = center
        self.previous_position = center

        self.path = deque(maxlen=500)

        self.path.append(center)

        # -------------------------
        # Time
        # -------------------------

        self.first_seen = time.time()
        self.last_seen = time.time()

        # -------------------------
        # Movement
        # -------------------------

        self.total_distance = 0.0

        self.current_speed = 0.0

        self.average_speed = 0.0

        self.frame_count = 1

        # -------------------------
        # Entry / Exit
        # -------------------------

        self.crossed = False

        self.entered = False

        self.exited = False

        # -------------------------
        # Zone
        # -------------------------

        self.current_zone = "Unknown"

        self.previous_zone = "Unknown"

        self.zone_enter_time = time.time()

        # -------------------------
        # Direction
        # -------------------------

        self.direction = "Unknown"

    # ==================================================
    # Update Position
    # ==================================================

    def update(self, center):

        self.previous_position = self.current_position

        self.current_position = center

        self.last_seen = time.time()

        self.frame_count += 1

        self.path.append(center)

        self.calculate_distance()

        self.calculate_speed()

        self.calculate_direction()

    # ==================================================
    # Distance
    # ==================================================

    def calculate_distance(self):

        x1, y1 = self.previous_position

        x2, y2 = self.current_position

        distance = math.sqrt(

            (x2 - x1) ** 2 +

            (y2 - y1) ** 2

        )

        self.total_distance += distance

    # ==================================================
    # Speed
    # ==================================================

    def calculate_speed(self):

        dt = max(

            self.last_seen - self.first_seen,

            0.001

        )

        self.current_speed = self.total_distance / dt

        self.average_speed = (

            self.total_distance /

            max(self.frame_count, 1)

        )

    # ==================================================
    # Direction
    # ==================================================

    def calculate_direction(self):

        x1, y1 = self.previous_position

        x2, y2 = self.current_position

        dx = x2 - x1

        dy = y2 - y1

        if abs(dx) > abs(dy):

            if dx > 0:

                self.direction = "Right"

            elif dx < 0:

                self.direction = "Left"

        else:

            if dy > 0:

                self.direction = "Down"

            elif dy < 0:

                self.direction = "Up"

    # ==================================================
    # Zone
    # ==================================================

    def update_zone(self, zone):

        if zone != self.current_zone:

            self.previous_zone = self.current_zone

            self.current_zone = zone

            self.zone_enter_time = time.time()

    # ==================================================
    # Dwell Time
    # ==================================================

    def dwell_time(self):

        return time.time() - self.first_seen

    # ==================================================
    # Zone Time
    # ==================================================

    def zone_time(self):

        return time.time() - self.zone_enter_time
    # ==========================================================
# Person Tracker
# ==========================================================

class PersonTracker:

    def __init__(self, max_history=60):

        self.people = {}

        self.max_history = max_history

        self.entry_count = 0

        self.exit_count = 0

        self.total_unique_people = set()

    # =====================================================
    # Update Person
    # =====================================================

    def update(self, person_id, center, line_x):

        if person_id not in self.people:

            self.people[person_id] = Person(
                person_id,
                center
            )

            self.total_unique_people.add(person_id)

        else:

            self.people[person_id].update(center)

        self.check_entry_exit(
            person_id,
            line_x
        )

    # =====================================================
    # Entry / Exit Detection
    # =====================================================

    def check_entry_exit(
        self,
        person_id,
        line_x
    ):

        person = self.people[person_id]

        px = person.previous_position[0]

        cx = person.current_position[0]

        if person.crossed:
            return

        # Left -> Right
        if px < line_x <= cx:

            self.entry_count += 1

            person.entered = True

            person.crossed = True

        # Right -> Left
        elif px > line_x >= cx:

            self.exit_count += 1

            person.exited = True

            person.crossed = True

    # =====================================================
    # Zone Update
    # =====================================================

    def update_zone(
        self,
        person_id,
        zone
    ):

        if person_id in self.people:

            self.people[person_id].update_zone(zone)

    # =====================================================
    # Cleanup Lost Tracks
    # =====================================================

    def cleanup(
        self,
        timeout=30
    ):

        current_time = time.time()

        remove_ids = []

        for pid, person in self.people.items():

            if current_time - person.last_seen > timeout:

                remove_ids.append(pid)

        for pid in remove_ids:

            del self.people[pid]

    # =====================================================
    # Current Crowd
    # =====================================================

    def current_people(self):

        return len(self.people)

    # =====================================================
    # Total Visitors
    # =====================================================

    def total_visitors(self):

        return len(self.total_unique_people)

    # =====================================================
    # Person Exists
    # =====================================================

    def exists(self, person_id):

        return person_id in self.people

    # =====================================================
    # Get Person
    # =====================================================

    def get(self, person_id):

        return self.people.get(person_id)

    # =====================================================
    # Path
    # =====================================================

    def get_path(self, person_id):

        if person_id not in self.people:

            return []

        return list(

            self.people[person_id].path

        )

    # =====================================================
    # Speed
    # =====================================================

    def get_speed(self, person_id):

        if person_id not in self.people:

            return 0

        return round(

            self.people[person_id].current_speed,

            2

        )

    # =====================================================
    # Average Speed
    # =====================================================

    def get_average_speed(self, person_id):

        if person_id not in self.people:

            return 0

        return round(

            self.people[person_id].average_speed,

            2

        )

    # =====================================================
    # Distance
    # =====================================================

    def get_distance(self, person_id):

        if person_id not in self.people:

            return 0

        return round(

            self.people[person_id].total_distance,

            2

        )

    # =====================================================
    # Dwell Time
    # =====================================================

    def get_dwell_time(self, person_id):

        if person_id not in self.people:

            return 0

        return round(

            self.people[person_id].dwell_time(),

            2

        )

    # =====================================================
    # Direction
    # =====================================================

    def get_direction(self, person_id):

        if person_id not in self.people:

            return "Unknown"

        return self.people[person_id].direction

    # =====================================================
    # Current Zone
    # =====================================================

    def get_zone(self, person_id):

        if person_id not in self.people:

            return "Unknown"

        return self.people[person_id].current_zone
        # =====================================================
    # Zone Time
    # =====================================================

    def get_zone_time(self, person_id):

        if person_id not in self.people:
            return 0

        return round(
            self.people[person_id].zone_time(),
            2
        )

    # =====================================================
    # Person Statistics
    # =====================================================

    def statistics(self):

        stats = []

        for pid, person in self.people.items():

            stats.append({

                "Person ID": person.id,

                "Distance": round(
                    person.total_distance,
                    2
                ),

                "Current Speed": round(
                    person.current_speed,
                    2
                ),

                "Average Speed": round(
                    person.average_speed,
                    2
                ),

                "Direction": person.direction,

                "Dwell Time": round(
                    person.dwell_time(),
                    2
                ),

                "Current Zone": person.current_zone,

                "Zone Time": round(
                    person.zone_time(),
                    2
                ),

                "Frames": person.frame_count

            })

        return stats

    # =====================================================
    # Tracker Summary
    # =====================================================

    def summary(self):

        return {

            "Current People": self.current_people(),

            "Unique Visitors": self.total_visitors(),

            "Entries": self.entry_count,

            "Exits": self.exit_count

        }

    # =====================================================
    # Reset Tracker
    # =====================================================

    def reset(self):

        self.people.clear()

        self.total_unique_people.clear()

        self.entry_count = 0

        self.exit_count = 0

    # =====================================================
    # Debug
    # =====================================================

    def print_summary(self):

        print("\n" + "=" * 50)

        print("TRACKER SUMMARY")

        print("=" * 50)

        print(f"Current People : {self.current_people()}")

        print(f"Unique Visitors: {self.total_visitors()}")

        print(f"Entries        : {self.entry_count}")

        print(f"Exits          : {self.exit_count}")

        print("=" * 50)

    # =====================================================
    # Iterable Support
    # =====================================================

    def __len__(self):

        return len(self.people)

    def __contains__(self, person_id):

        return person_id in self.people

    def __getitem__(self, person_id):

        return self.people[person_id]

    def __iter__(self):

        return iter(self.people.values())