# Assignment
##
## Unit tests for the Event class
## Tests for Event File
## Author: Wisdom Ogbeche

import unittest
from event import Event

class TestEvent(unittest.TestCase):

    def setUp(self):
        """Creates a valid event before each test."""
        self.event = Event("Open Mic Night", "The Cluny", "2026-11-14", 120,
                            {"standard": 5.0, "vip": 12.5}, {"standard": 75}, "music", False)

    # Normal Cases

    def test_get_name(self):
        self.assertEqual(self.event.get_name(), "Open Mic Night")

    def test_get_venue(self):
        self.assertEqual(self.event.get_venue(), "The Cluny")

    def test_get_date(self):
        self.assertEqual(self.event.get_date(), "2026-11-14")

    def test_get_capacity(self):
        self.assertEqual(self.event.get_capacity(), 120)

    def test_get_ticket_prices(self):
        self.assertEqual(self.event.get_ticket_prices(), {"standard": 5.0, "vip": 12.5})

    def test_get_tickets_sold(self):
        self.assertEqual(self.event.get_tickets_sold(), {"standard": 75})

    def test_get_category(self):
        self.assertEqual(self.event.get_category(), "music")

    def test_get_family_friendly(self):
        self.assertEqual(self.event.get_family_friendly(), False)

    def test_total_tickets_sold(self):
        """75 tickets have been sold."""
        self.assertEqual(self.event.get_total_tickets_sold(), 75)

    def test_tickets_remaining(self):
        """120 capacity - 75 sold = 45 remaining."""
        self.assertEqual(self.event.get_tickets_remaining(), 45)

    def test_total_revenue(self):
        """75 * 5.0 + 0 * 12.5 = 375.0, the example from the specification."""
        self.assertEqual(self.event.get_total_revenue(), 375.0)

    def test_total_revenue_rounded(self):
        """Total revenue is rounded to 2 decimal places."""
        event = Event("Test Event", "Test Venue", "2026-11-14", 10,
                      {"standard": 1.111}, {"standard": 3}, "music", False)
        self.assertEqual(event.get_total_revenue(), 3.33)

    def test_str(self):
        """str() matches the format in the specification."""
        expected = ("Open Mic Night,The Cluny,2026-11-14,120,{'standard': 5.0, 'vip': 12.5},"
                    "{'standard': 75},music,False")
        self.assertEqual(str(self.event), expected)

    def test_repr(self):
        """repr() shows the code that creates the event."""
        expected = ("Event('Open Mic Night', 'The Cluny', '2026-11-14', 120, "
                    "{'standard': 5.0, 'vip': 12.5}, {'standard': 75}, 'music', False)")
        self.assertEqual(repr(self.event), expected)

    def test_equal(self):
        """Same name, venue and date means equal, even if other details differ."""
        other = Event("Open Mic Night", "The Cluny", "2026-11-14", 50,
                      {"standard": 1.0}, {}, "comedy", True)
        self.assertEqual(self.event, other)
        self.assertEqual(hash(self.event), hash(other))

    def test_not_equal_(self):
        """A different date means not equal."""
        other = Event("Open Mic Night", "The Cluny", "2026-11-15", 120,
                      {"standard": 5.0}, {}, "music", False)
        self.assertNotEqual(self.event, other)

    def test_not_equal_venue(self):
        """A different venue means the events are not equal."""
        other = Event("Open Mic Night", "O2 Academy", "2026-11-14", 120,
                       {"standard": 5.0}, {}, "music", False)
        self.assertNotEqual(self.event, other)

    def test_not_equal_name(self):
        """A different name means the events are not equal."""
        other = Event("Jazz Night", "The Cluny", "2026-11-14", 120,
                       {"standard": 5.0}, {}, "music", False)
        self.assertNotEqual(self.event, other)

    # Boundary cases

    def test_exactly_sold_out(self):
        """Selling exactly the capacity is allowed and leaves 0 remaining."""
        event = Event("Comedy Late Show", "The Stand", "2026-11-20", 150,
                      {"standard": 18.0}, {"standard": 150}, "comedy", False)
        self.assertEqual(event.get_tickets_remaining(), 0)

    def test_empty_tickets_sold(self):
        """An empty tickets_sold means 0 sold and 0.0 revenue."""
        event = Event("Robotics Workshop", "Urban Sciences Building", "2026-10-03", 60,
                      {"standard": 15.0}, {}, "education", True)
        self.assertEqual(event.get_total_tickets_sold(), 0)
        self.assertEqual(event.get_total_revenue(), 0.0)

    # Exceptional cases

    def test_name_not_string(self):
        """A name that is not a string raises ValueError."""
        with self.assertRaises(ValueError):
            Event(123, "The Cluny", "2026-11-14", 120, {"standard": 5.0}, {}, "music", False)

    def test_capacity_zero(self):
        """A capacity of 0 raises ValueError."""
        with self.assertRaises(ValueError):
            Event("Open Mic Night", "The Cluny", "2026-11-14", 0, {"standard": 5.0}, {}, "music", False)

    def test_capacity_not_int(self):
        """A capacity that is not an int raises ValueError."""
        with self.assertRaises(ValueError):
            Event("Open Mic Night", "The Cluny", "2026-11-14", "120", {"standard": 5.0}, {}, "music", False)

    def test_no_ticket_tiers(self):
        """An empty ticket_prices raises ValueError."""
        with self.assertRaises(ValueError):
            Event("Open Mic Night", "The Cluny", "2026-11-14", 120, {}, {}, "music", False)

    def test_price_not_positive(self):
        """A price of 0 raises ValueError."""
        with self.assertRaises(ValueError):
            Event("Open Mic Night", "The Cluny", "2026-11-14", 120, {"standard": 0.0}, {}, "music", False)

    def test_sold_tier_not_in_prices(self):
        """Selling a tier that has no price raises ValueError."""
        with self.assertRaises(ValueError):
            Event("Open Mic Night", "The Cluny", "2026-11-14", 120, {"standard": 5.0}, {"vip": 1}, "music", False)

    def test_negative_tickets_sold(self):
        """A negative tickets sold value raises ValueError."""
        with self.assertRaises(ValueError):
            Event("Open Mic Night", "The Cluny", "2026-11-14", 120, {"standard": 5.0}, {"standard": -1}, "music", False)

    def test_sold_more_than_capacity(self):
        """Selling more tickets than the capacity raises ValueError."""
        with self.assertRaises(ValueError):
            Event("Open Mic Night", "The Cluny", "2026-11-14", 120, {"standard": 5.0}, {"standard": 121}, "music",
                  False)

    def test_family_friendly_not_bool(self):
        """A family_friendly value that is not True/False raises ValueError."""
        with self.assertRaises(ValueError):
            Event("Open Mic Night", "The Cluny", "2026-11-14", 120, {"standard": 5.0}, {}, "music", "yes")

if __name__ == "__main__":
    unittest.main();