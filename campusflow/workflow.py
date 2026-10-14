"""
CampusFlow ticket workflow.

Engineer B:
- Ticket assignment
- Status transitions
- Ticket reopening
- Ordered work queue
"""


# Allowed ticket statuses
VALID_STATUSES = {"open", "in_progress", "resolved"}

# Priority order for the work queue
PRIORITY_ORDER = {
    "critical": 0,
    "high": 1,
    "medium": 2,
    "low": 3,
}


def find_ticket(tickets, ticket_id):
    """
    Find and return a ticket using its ID.

    Raises ValueError if the ticket does not exist.
    """
    for ticket in tickets:
        if ticket["id"] == ticket_id:
            return ticket

    raise ValueError(f"Ticket '{ticket_id}' was not found.")


def assign_ticket(tickets, ticket_id, staff_name):
    """
    Assign a ticket to a staff member.

    The staff member's name must not be empty.
    Resolved tickets must be reopened before modification.

    Returns the updated ticket.
    """
    if not isinstance(staff_name, str) or not staff_name.strip():
        raise ValueError("Staff member name cannot be empty.")

    ticket = find_ticket(tickets, ticket_id)

    if ticket["status"] == "resolved":
        raise ValueError(
            "Cannot assign a resolved ticket. Reopen it first."
        )

    ticket["assigned_to"] = staff_name.strip()

    return ticket


def update_status(tickets, ticket_id, new_status):
    """
    Change a ticket's status.

    Allowed transitions:
        open -> in_progress
        in_progress -> resolved

    An unassigned ticket cannot move to in_progress.

    Resolved tickets must be explicitly reopened before
    another status change.

    Returns the updated ticket.
    """
    if not isinstance(new_status, str):
        raise ValueError("Status must be a string.")

    new_status = new_status.strip().lower()

    if new_status not in VALID_STATUSES:
        raise ValueError(
            f"Invalid status '{new_status}'. "
            f"Allowed statuses: {', '.join(sorted(VALID_STATUSES))}."
        )

    ticket = find_ticket(tickets, ticket_id)

    current_status = ticket["status"]

    if current_status == "resolved":
        raise ValueError(
            "Resolved tickets must be explicitly reopened first."
        )

    if current_status == "open" and new_status == "in_progress":
        if not ticket["assigned_to"]:
            raise ValueError(
                "Cannot start work on an unassigned ticket."
            )

        ticket["status"] = "in_progress"
        return ticket

    if current_status == "in_progress" and new_status == "resolved":
        ticket["status"] = "resolved"
        return ticket

    raise ValueError(
        f"Invalid status transition: "
        f"{current_status} -> {new_status}."
    )


def reopen_ticket(tickets, ticket_id):
    """
    Explicitly reopen a resolved ticket.

    The ticket's status becomes open.

    Returns the updated ticket.
    """
    ticket = find_ticket(tickets, ticket_id)

    if ticket["status"] != "resolved":
        raise ValueError(
            "Only resolved tickets can be reopened."
        )

    ticket["status"] = "open"

    return ticket


def get_work_queue(tickets):
    """
    Return unresolved tickets ordered by:

    1. Priority: critical, high, medium, low.
    2. Numeric ticket ID: earlier IDs first.

    Only open tickets are included. Tickets in progress
    are also unresolved, so they remain in the queue.
    Resolved tickets are excluded.

    The original ticket list is not modified.
    """
    unresolved_tickets = [
        ticket
        for ticket in tickets
        if ticket["status"] in {"open", "in_progress"}
    ]

    def queue_sort_key(ticket):
        priority = ticket["priority"].lower()

        if priority not in PRIORITY_ORDER:
            raise ValueError(
                f"Unknown ticket priority: {ticket['priority']}"
            )

        # T001 -> 1, T012 -> 12
        ticket_number = int(ticket["id"][1:])

        return PRIORITY_ORDER[priority], ticket_number

    return sorted(unresolved_tickets, key=queue_sort_key)