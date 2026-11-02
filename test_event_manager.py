# Assignment
##
## Unit tests for the Event class
## Tests for Event_Manager File
## Author: Wisdom Ogbeche


import os
import unittest

from event import Event
from event_manager import EventManager

class TestEventManager(unittest.TestCase):
    """Tests for the EventManager class."""

    def setUp(self):
        """Create four events and a manager holding them before each test."""

        # music, family friendly, revenue 180*25 + 40*60 = 6900.0, 280 remaining
        self.gala = Event("Winter Gala", "City Hall, Newcastle", "2026-12-05", 500,
                          {"standard": 25.0, "vip": 60.0}, {"standard": 180, "vip": 40}, "music", True)

        # music, adults only, revenue 75*5 = 375.0, 45 remaining
        self.open_mic = Event("Open Mic Night", "The Cluny", "2026-11-14", 120,
                              {"standard": 5.0, "vip": 12.5}, {"standard": 75}, "music", False)

        # education, family friendly, revenue 0.0, 60 remaining
        self.workshop = Event("Robotics Workshop", "Urban Sciences Building", "2026-10-03", 60,
                              {"standard": 15.0}, {}, "education", True)

        # comedy, adults only, sold out, revenue 150*18 = 2700.0, 0 remaining
        self.comedy = Event("Comedy Late Show", "The Stand", "2026-11-20", 150,
                            {"standard": 18.0}, {"standard": 150}, "comedy", False)


        self.manager = EventManager([self.gala, self.open_mic, self.workshop, self.comedy])

    # Constructor and get_events

    def test_empty_manager(self):
        """A manager created with no events has an empty list."""
        self.assertEqual(EventManager().get_events(), [])

    def test_get_events(self):
        """get_events returns all events in order."""
        self.assertEqual(self.manager.get_events(), [self.gala, self.open_mic, self.workshop, self.comedy])

    def test_add_event(self):
        """A new event is added."""
        event = Event("Spelling Bee ", "The Cumberland Arms", "2026-10-29", 80,
                      {"standard": 8.0}, {"standard": 34}, "literature", False)
        self.manager.add_event(event)
        self.assertIn(event, self.manager.get_events())

    def test_add_same_name_different_date(self):
        """The same name on a different date is not a duplicate."""
        event = Event("Winter Gala", "City Hall, Newcastle", "2027-01-16", 600,
                      {"standard": 30.0}, {}, "music", True)
        self.manager.add_event(event)
        self.assertEqual(len(self.manager.search_by_name("Winter Gala")), 2)

    def test_add_duplicate(self):
        """Adding an event with the same name, venue and date raises ValueError."""
        duplicate = Event("Winter Gala", "City Hall, Newcastle", "2026-12-05", 10,
                          {"standard": 1.0}, {}, "music", True)
        with self.assertRaises(ValueError):
            self.manager.add_event(duplicate)

    def test_add_not_an_event(self):
        """Adding something that is not an Event raises ValueError."""
        with self.assertRaises(ValueError):
            self.manager.add_event("Winter Gala")

    def test_remove_event(self):
        """An existing event is removed."""
        self.manager.remove_event(self.gala)
        self.assertNotIn(self.gala, self.manager.get_events())

    def test_remove_missing_event(self):
        """Removing an event that is not there changes nothing."""
        manager = EventManager([self.gala])
        manager.remove_event(self.comedy)
        self.assertEqual(manager.get_events(), [self.gala])

    def test_edit_event(self):
        """old_event is replaced by new_event."""
        new_event = Event("Spelling Bee", "The Cumberland Arms", "2026-10-29", 80,
                          {"standard": 8.0}, {}, "literature", False)
        self.manager.edit_event(self.gala, new_event)
        self.assertIn(new_event, self.manager.get_events())
        self.assertNotIn(self.gala, self.manager.get_events())

    def test_edit_keeping_same_name_venue_date(self):
        """new_event may have the same name, venue and date as old_event."""
        updated = Event("Winter Gala", "City Hall, Newcastle", "2026-12-05", 500,
                        {"standard": 25.0, "vip": 60.0}, {"standard": 200}, "music", True)
        self.manager.edit_event(self.gala, updated)
        self.assertEqual(self.manager.get_events()[0].get_tickets_sold(), {"standard": 200})

    def test_edit_old_event_missing(self):
        """Editing an event that does not exist raises ValueError."""
        manager = EventManager([self.gala])
        with self.assertRaises(ValueError):
            manager.edit_event(self.comedy, self.workshop)

    def test_edit_into_duplicate(self):
        """Editing an event into a copy of another event raises ValueError."""
        with self.assertRaises(ValueError):
            self.manager.edit_event(self.gala, self.open_mic)

    # Searches and Filters

    def test_search_by_name(self):
        """Only the event with the exact name is returned."""
        self.assertEqual(self.manager.search_by_name("Open Mic Night"), [self.open_mic])
        self.assertEqual(self.manager.search_by_name("Open Mic"), [])

    def test_search_by_revenue(self):
        """Events with revenue in the range are returned."""
        self.assertEqual(self.manager.search_by_revenue(300, 3000), [self.open_mic, self.comedy])

    def test_search_by_revenue_exact_bounds(self):
        """Boundary: revenue exactly equal to the bounds is included."""
        self.assertEqual(self.manager.search_by_revenue(375.0, 2700.0), [self.open_mic, self.comedy])

    def test_search_by_revenue_min_greater_than_max(self):
        """min_revenue greater than max_revenue raises ValueError."""
        with self.assertRaises(ValueError):
            self.manager.search_by_revenue(100, 50)

    def test_category_and_family_friendly(self):
        """Only events matching both category and family_friendly are returned."""
        self.assertEqual(self.manager.get_events_by_category_and_family_friendly("music", True), [self.gala])
        self.assertEqual(self.manager.get_events_by_category_and_family_friendly("music", False), [self.open_mic])

    # Reports

    def test_revenue_per_category(self):
        """Revenue is totalled for each category."""
        expected = {"music": 7275.0, "education": 0.0, "comedy": 2700.0}
        self.assertEqual(self.manager.get_revenue_per_category(), expected)

    def test_tickets_remaining_by_category(self):
        """Tickets remaining are totalled for each category."""
        expected = {"music": 325, "education": 60, "comedy": 0}
        self.assertEqual(self.manager.get_tickets_remaining_by_category(), expected)

    # Files

    def test_load_from_file(self):
        """Valid rows are loaded; bad and duplicate rows in test_events.csv are skipped."""
        manager = EventManager()
        manager.load_from_file("test_events.csv")
        self.assertEqual(manager.get_events(), [self.gala, self.open_mic, self.workshop, self.comedy])
        self.assertEqual(manager.get_events()[0].get_venue(), "City Hall, Newcastle")

    def test_save_then_load(self):
        """Saving then loading gives back the same events with the same details."""
        self.manager.save_to_file("test_output.csv")
        loaded = EventManager()
        loaded.load_from_file("test_output.csv")
        os.remove("test_output.csv")  # tidy up the file this test created
        self.assertEqual(repr(loaded), repr(self.manager))


if __name__ == "__main__":
    unittest.main()
