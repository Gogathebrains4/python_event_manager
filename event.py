# Assignment
##
## Manage the details and ticket sales of a single event
## Event File
## Author: Wisdom Ogbeche

class Event:
    """A ticketed event held at a venue on a given date."""

    def __init__(self, name, venue, date, capacity, ticket_prices, tickets_sold, category, family_friendly):
        """Validate inputs. Raise ValueError if any argument breaks the rules."""

        if type(name) != str:
            raise ValueError("name must be a string")
        if type(venue) != str:
            raise ValueError("venue must be a string")
        if type(date) != str:
            raise ValueError("date must be a string")

        # Capacity must be a whole number above 0
        if type(capacity) != int or capacity <= 0:
            raise ValueError("capacity must be an int greater than 0")

        # Ticket prices must contain at least one tier, and every price must be a float above 0
        if type(ticket_prices) != dict or len(ticket_prices) == 0:
            raise ValueError("ticket_prices must be a dict with at least one tier")
        for tier in ticket_prices:
            if type(tier) != str:
                raise ValueError("tier names must be strings")
            price = ticket_prices[tier]
            if type(price) != float or price <= 0:
                raise ValueError(f"price for tier '{tier}' must be a float greater than 0")

        # Every tier sold must exist in ticket_prices and every count must be an int of 0 or more
        if type(tickets_sold) != dict:
            raise ValueError('tickets sold must be a dict')
        total_sold = 0
        for tier in tickets_sold:
            if tier not in ticket_prices:
                raise ValueError(f"tier '{tier}' in tickets_sold is not in ticket_prices")
            sold = tickets_sold[tier]
            if type(sold) != int or sold < 0:
                raise ValueError(f"tickets sold for tier '{tier}' must be an int of 0 or more")
            total_sold += sold

        # The total sold across all tiers cannot be more than the capacity
        if total_sold > capacity:
             raise ValueError(f"total tickets sold {total_sold} is more than capacity {capacity}")

        if type(category) != str:
            raise ValueError("category must be a string")

        if type(family_friendly) != bool:
            raise ValueError("family_friendly must be True or False")

        # Everything is valid, so store it in private attributes
        self.name = name
        self.venue = venue
        self.date = date
        self.capacity = capacity
        self.ticket_prices = dict(ticket_prices)  # store a copy, not the caller's dict
        self.tickets_sold = dict(tickets_sold)
        self.category = category
        self.family_friendly = family_friendly

    def get_name(self):
        """Return the event name."""
        return self.name

    def get_venue(self):
        """Return the venue name."""
        return self.venue

    def get_date(self):
        """Return the date as a YYYY-MM-DD string."""
        return self.date

    def get_capacity(self):
        """Return the maximum number of tickets."""
        return self.capacity

    def get_ticket_prices(self):
        """Return a copy of the ticket prices dict."""
        return dict(self.ticket_prices)

    def get_tickets_sold(self):
        """Return a copy of the tickets sold dict."""
        return dict(self.tickets_sold)

    def get_category(self):
        """Return the category."""
        return self.category

    def get_family_friendly(self):
        """Return True if suitable for all ages, False if adults only."""
        return self.family_friendly

    def __str__(self):
        """Return the event details as a comma separated string."""
        return (f"{self.name},{self.venue},{self.date},{self.capacity},"
                f"{self.ticket_prices},{self.tickets_sold},{self.category},{self.family_friendly}")

    def __repr__(self):
        """Return the code that would create this event."""
        return (f"Event({self.name!r}, {self.venue!r}, {self.date!r}, {self.capacity!r}, "
                f"{self.ticket_prices!r}, {self.tickets_sold!r}, {self.category!r}, "
                f"{self.family_friendly!r})")

    def __eq__(self, other):
        """Return True if other has the same name, venue and date."""
        if not isinstance(other, Event):
            return False
        return (self.name == other.get_name()
                and self.venue == other.get_venue()
                and self.date == other.get_date())

    def __hash__(self):
        """Return a hash made from the same fields used by __eq__."""
        return hash((self.name, self.venue, self.date))

    def get_total_tickets_sold(self):
        """Return the total tickets sold across all tiers."""
        total_tickets_sold = 0
        for tier in self.tickets_sold:
            total_tickets_sold += self.tickets_sold[tier]
        return total_tickets_sold

    def get_tickets_remaining(self):
        """Return capacity minus total tickets sold."""
        return self.capacity - self.get_total_tickets_sold()

    def get_total_revenue(self):
        """Return the total revenue, rounded to 2 decimal places."""
        revenue = 0.0
        for tier in self.tickets_sold:
            revenue += self.tickets_sold[tier] * self.ticket_prices[tier]
        return round(revenue, 2)
