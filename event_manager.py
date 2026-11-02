# Assignment
##
## Manage a collection of events
## Event Manger File
## Author: Wisdom Ogbeche

import csv

from event import Event

class EventManager:
    """Stores events and lets you add, edit, remove, search, report on and save them."""

    def __init__(self, events=None):
        """Create the manager with the given list of events, or an empty list."""
        if events is None:
            self.__events = []
        else:
            self.__events = list(events)  # store a copy of the list

    def get_events(self):
        """Return a copy of the list of events."""
        return list(self.__events)

    def __str__(self):
        """Return every event, one per line."""
        text = ""
        for event in self.__events:
            text += str(event) + "\n"
        return text`

    def __repr__(self):
        """Return the code that would create this manager."""
        return f"EventManager({self.__events!r})"

    def add_event(self, event):
        """Add an event. Raise ValueError if it is not an Event or is a duplicate."""
        if not isinstance(event, Event):
            raise ValueError("event must be an Event")
        if event in self.__events:
            raise ValueError("an event with this name, venue and date already exists")
        self.__events.append(event)

    def remove_event(self, event):
        """Remove the event if it exists."""
        if event in self.__events:
            self.__events.remove(event)

    def edit_event(self, old_event, new_event):
        """Replace old_event with new_event. Raise ValueError if this breaks the rules."""
        if old_event not in self.__events:
            raise ValueError("old_event does not exist")
        if not isinstance(new_event, Event):
            raise ValueError("new_event must be an Event")
        # new_event may match old_event, but not any other event
        for event in self.__events:
            if event != old_event and event == new_event:
                raise ValueError("an event with this name, venue and date already exists")
        position = self.__events.index(old_event)
        self.__events[position] = new_event

    def search_by_name(self, name):
        """Return a list of events whose name exactly matches name."""
        results = []
        for event in self.__events:
            if event.get_name() == name:
                results.append(event)
        return results

    def search_by_revenue(self, min_revenue, max_revenue):
        """Return a list of events with revenue between or equal to min_revenue and max_revenue."""
        if min_revenue > max_revenue:
            raise ValueError("min_revenue cannot be greater than max_revenue")
        results = []
        for event in self.__events:
            revenue = round(event.get_total_revenue(), 2)
            if min_revenue <= revenue <= max_revenue:
                results.append(event)
        return results

    def get_events_by_category_and_family_friendly(self, category, family_friendly):
        """Return a list of events matching both category and family_friendly."""
        results = []
        for event in self.__events:
            if event.get_category() == category and event.get_family_friendly() == family_friendly:
                results.append(event)
        return results

    def get_revenue_per_category(self):
        """Return a dict mapping each category to its total revenue."""
        totals = {}
        for event in self.__events:
            category = event.get_category()
            if category not in totals:
                totals[category] = 0.0
            totals[category] += event.get_total_revenue()
        # Round each total to 2 decimal places
        for category in totals:
            totals[category] = round(totals[category], 2)
        return totals

    def get_tickets_remaining_by_category(self):
        """Return a dict mapping each category to its total tickets remaining."""
        totals = {}
        for event in self.__events:
            category = event.get_category()
            if category not in totals:
                totals[category] = 0
            totals[category] += event.get_tickets_remaining()
        return totals

    def load_from_file(self, file_name):
        """Read events from a CSV file and add valid, non-duplicate events."""

        with open(file_name, "r", newline="") as file:
            reader = csv.reader(file)
            next(reader, None)  # Skip the header row

            for row in reader:
                try:
                    # Check that the row has all 8 fields
                    if len(row) != 8:
                        continue

                    capacity = int(row[3])

                    # Convert ticket prices into a dictionary
                    ticket_prices = {}
                    for pair in row[4].split(";"):
                        tier, price = pair.split(":")
                        ticket_prices[tier] = float(price)

                    # Convert tickets sold into a dictionary
                    tickets_sold = {}
                    if row[5] != "":
                        for pair in row[5].split(";"):
                            tier, sold = pair.split(":")
                            tickets_sold[tier] = int(sold)

                    # Convert family-friendly string into a Boolean
                    if row[7].lower() == "true":
                        family_friendly = True
                    elif row[7].lower() == "false":
                        family_friendly = False
                    else:
                        raise ValueError("family_friendly must be True or False")

                    # Create the event
                    event = Event(row[0], row[1], row[2], capacity, ticket_prices, tickets_sold, row[6],
                        family_friendly)

                    # Add the event; skip it if it is invalid or duplicated
                    self.add_event(event)

                except (ValueError, IndexError, TypeError):
                    # Bad row (wrong value, missing field, invalid or duplicate event): skip
                    continue

    def save_to_file(self, file_name):
        """Write all events to a csv file."""
        with open(file_name, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["name", "venue", "date", "capacity", "ticket_prices",
                             "tickets_sold", "category", "family_friendly"])

            for event in self.__events:
                # {"standard": 25.0, "vip": 60.0} -> "standard:25.0;vip:60.0"
                price_parts = []
                prices = event.get_ticket_prices()
                for tier in prices:
                    price_parts.append(f"{tier}:{prices[tier]}")

                sold_parts = []
                sold = event.get_tickets_sold()
                for tier in sold:
                    sold_parts.append(f"{tier}:{sold[tier]}")

                writer.writerow([event.get_name(), event.get_venue(), event.get_date(),
                                 event.get_capacity(), ";".join(price_parts), ";".join(sold_parts),
                                 event.get_category(), event.get_family_friendly()])
