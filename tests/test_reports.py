import unittest

from campusflow.reports import generate_report


def make_ticket(ticket_id, status, priority):
    """Create a sample ticket for report testing."""
    return {
        "id": ticket_id,
        "title": "Sample ticket",
        "category": "Software",
        "urgency": "medium",
        "affected_users": 3,
        "priority": priority,
        "status": status,
        "assigned_to": None,
    }


class TestReports(unittest.TestCase):

    def test_empty_report(self):
        report = generate_report([])

        self.assertEqual(report["total_tickets"], 0)

        self.assertEqual(
            report["by_status"],
            {
                "open": 0,
                "in_progress": 0,
                "resolved": 0,
            },
        )

        self.assertEqual(
            report["by_priority"],
            {
                "critical": 0,
                "high": 0,
                "medium": 0,
                "low": 0,
            },
        )

    def test_total_ticket_count(self):
        tickets = [
            make_ticket("T001", "open", "critical"),
            make_ticket("T002", "in_progress", "high"),
            make_ticket("T003", "resolved", "low"),
        ]

        report = generate_report(tickets)

        self.assertEqual(report["total_tickets"], 3)

    def test_status_breakdown(self):
        tickets = [
            make_ticket("T001", "open", "high"),
            make_ticket("T002", "open", "low"),
            make_ticket("T003", "resolved", "medium"),
            make_ticket("T004", "in_progress", "critical"),
        ]

        report = generate_report(tickets)

        self.assertEqual(
            report["by_status"],
            {
                "open": 2,
                "in_progress": 1,
                "resolved": 1,
            },
        )

    def test_priority_breakdown(self):
        tickets = [
            make_ticket("T001", "open", "critical"),
            make_ticket("T002", "open", "critical"),
            make_ticket("T003", "resolved", "high"),
            make_ticket("T004", "in_progress", "low"),
        ]

        report = generate_report(tickets)

        self.assertEqual(
            report["by_priority"],
            {
                "critical": 2,
                "high": 1,
                "medium": 0,
                "low": 1,
            },
        )

    def test_invalid_status_is_rejected(self):
        tickets = [
            make_ticket("T001", "cancelled", "low")
        ]

        with self.assertRaises(ValueError):
            generate_report(tickets)

    def test_invalid_priority_is_rejected(self):
        tickets = [
            make_ticket("T001", "open", "urgent")
        ]

        with self.assertRaises(ValueError):
            generate_report(tickets)


if __name__ == "__main__":
    unittest.main()