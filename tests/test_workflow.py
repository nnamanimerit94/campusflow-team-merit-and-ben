import unittest

from campusflow.workflow import (
    assign_ticket,
    update_status,
    reopen_ticket,
    get_work_queue,
)


def make_ticket(
    ticket_id="T001",
    priority="medium",
    status="open",
    assigned_to=None,
):
    """Create a sample ticket for testing."""
    return {
        "id": ticket_id,
        "title": "Sample ticket",
        "category": "Software",
        "urgency": "medium",
        "affected_users": 3,
        "priority": priority,
        "status": status,
        "assigned_to": assigned_to,
    }


class TestTicketAssignment(unittest.TestCase):

    def setUp(self):
        self.tickets = [make_ticket()]

    def test_assign_ticket_successfully(self):
        ticket = assign_ticket(
            self.tickets, "T001", "Ada"
        )

        self.assertEqual(ticket["assigned_to"], "Ada")

    def test_assignment_removes_extra_whitespace(self):
        ticket = assign_ticket(
            self.tickets, "T001", "  Ada  "
        )

        self.assertEqual(ticket["assigned_to"], "Ada")

    def test_reject_blank_staff_name(self):
        with self.assertRaises(ValueError):
            assign_ticket(self.tickets, "T001", "   ")

    def test_reject_unknown_ticket_id(self):
        with self.assertRaises(ValueError):
            assign_ticket(self.tickets, "T999", "Ada")

    def test_resolved_ticket_cannot_be_assigned(self):
        self.tickets[0]["status"] = "resolved"

        with self.assertRaises(ValueError):
            assign_ticket(self.tickets, "T001", "Ada")


class TestTicketLifecycle(unittest.TestCase):

    def setUp(self):
        self.tickets = [make_ticket()]

    def test_unassigned_ticket_cannot_start_work(self):
        with self.assertRaises(ValueError):
            update_status(
                self.tickets, "T001", "in_progress"
            )

        # A rejected operation must not alter the status.
        self.assertEqual(
            self.tickets[0]["status"], "open"
        )

    def test_assigned_ticket_can_be_resolved(self):
        assign_ticket(self.tickets, "T001", "Ada")

        update_status(
            self.tickets, "T001", "in_progress"
        )

        self.assertEqual(
            self.tickets[0]["status"], "in_progress"
        )

        update_status(
            self.tickets, "T001", "resolved"
        )

        self.assertEqual(
            self.tickets[0]["status"], "resolved"
        )

    def test_cannot_skip_in_progress(self):
        assign_ticket(self.tickets, "T001", "Ada")

        with self.assertRaises(ValueError):
            update_status(
                self.tickets, "T001", "resolved"
            )

        self.assertEqual(
            self.tickets[0]["status"], "open"
        )

    def test_resolved_ticket_must_be_reopened(self):
        self.tickets[0]["status"] = "resolved"

        with self.assertRaises(ValueError):
            update_status(
                self.tickets, "T001", "open"
            )

    def test_reopen_resolved_ticket(self):
        self.tickets[0]["status"] = "resolved"

        ticket = reopen_ticket(self.tickets, "T001")

        self.assertEqual(ticket["status"], "open")

    def test_cannot_reopen_an_open_ticket(self):
        with self.assertRaises(ValueError):
            reopen_ticket(self.tickets, "T001")

    def test_invalid_status_is_rejected(self):
        with self.assertRaises(ValueError):
            update_status(
                self.tickets, "T001", "cancelled"
            )

        self.assertEqual(
            self.tickets[0]["status"], "open"
        )


class TestWorkQueue(unittest.TestCase):

    def setUp(self):
        self.tickets = [
            make_ticket("T010", "low"),
            make_ticket("T003", "critical"),
            make_ticket("T002", "high"),
            make_ticket("T001", "critical"),
            make_ticket("T004", "medium", "resolved"),
        ]

    def test_queue_sorts_by_priority_and_numeric_id(self):
        queue = get_work_queue(self.tickets)

        actual_ids = [
            ticket["id"] for ticket in queue
        ]

        self.assertEqual(
            actual_ids,
            ["T001", "T003", "T002", "T010"],
        )

    def test_resolved_tickets_are_excluded(self):
        queue = get_work_queue(self.tickets)

        actual_ids = [
            ticket["id"] for ticket in queue
        ]

        self.assertNotIn("T004", actual_ids)

    def test_queue_does_not_modify_original_list(self):
        original_ids = [
            ticket["id"] for ticket in self.tickets
        ]

        get_work_queue(self.tickets)

        updated_ids = [
            ticket["id"] for ticket in self.tickets
        ]

        self.assertEqual(updated_ids, original_ids)

    def test_in_progress_tickets_remain_in_queue(self):
        self.tickets[0]["status"] = "in_progress"

        queue = get_work_queue(self.tickets)

        actual_ids = [
            ticket["id"] for ticket in queue
        ]

        self.assertIn("T010", actual_ids)

    def test_empty_queue(self):
        self.assertEqual(get_work_queue([]), [])


if __name__ == "__main__":
    unittest.main()