"""Ваши проверки. Сначала рассчитайте ожидания по требованиям, затем пишите код."""

import unittest

from mediapolka import issue, new_state, return_loan


class StudentTests(unittest.TestCase):
    # Методы проверок должны называться test_...
    # Начинайте независимый тест с state = new_state().
    # Пример синтаксиса смотрите в test_start.py и в памятке.
    pass
    def test_issue_one_microphone(self):
        state = new_state()
        result = issue(state, "mic", "1")

        self.assertTrue(result["ok"])
        self.assertEqual(state["stock"]["mic"], 2)
        self.assertEqual(len(state["loans"]), 1)
        self.assertEqual(state["loans"][0]["status"], "issued")

    def test_issue_max_microphone_count(self):
        state = new_state()
        result = issue(state, "mic", "3")
        self.assertEqual(state["stock"]["mic"], 0)
        self.assertEqual(len(state["loans"]), 1)
        self.assertEqual(state["loans"][0]["status"], "issued")

    def test_issue_max_tripod_count(self):
        state = new_state()
        state["stock"]["tripod"] = 3
        result = issue(state, "tripod", "3")
        self.assertEqual(state["stock"]["tripod"], 0)
        self.assertEqual(len(state["loans"]), 1)
        self.assertEqual(state["loans"][0]["status"], "issued")

    def test_issue_max_light_count(self):
        state = new_state()
        state["stock"]["light"] = 3
        result = issue(state, "light", "3")
        self.assertEqual(state["stock"]["light"], 0)
        self.assertEqual(len(state["loans"]), 1)
        self.assertEqual(state["loans"][0]["status"], "issued")

    
    def test_issue_more_than_available_tripod(self):
        state = new_state()
        stock = state["stock"]["tripod"]
        result = issue(state, "tripod", (str)(state["stock"]["tripod"] + 1))
        self.assertEqual(state["stock"]["tripod"], stock)
        self.assertEqual(len(state["loans"]), 0)
        self.assertFalse(result["ok"])

    def test_issue_more_than_available_microphone(self):
        state = new_state()
        stock = state["stock"]["mic"]
        result = issue(state, "mic", (str)(state["stock"]["mic"] + 1))
        self.assertEqual(state["stock"]["mic"], stock)
        self.assertEqual(len(state["loans"]), 0)
        self.assertFalse(result["ok"])
    
    def test_issue_more_than_available_light(self):
        state = new_state()
        stock = state["stock"]["light"]
        result = issue(state, "light", (str)(state["stock"]["light"] + 1))
        self.assertEqual(state["stock"]["light"], stock)
        self.assertEqual(len(state["loans"]), 0)
        self.assertFalse(result["ok"])

    def test_return_returned_loan_tripod(self):
        state = new_state()
        loan = {
            "id": state["next_id"],
            "item": "tripod",
            "quantity": 1,
            "status": "returned",
        }
        state["loans"].append(loan)

        before_count = state["stock"]["tripod"]
        result = return_loan(state, loan["id"])
        self.assertEqual(before_count, state["stock"]["tripod"])

    def test_return_returned_loan_microphone(self):
        state = new_state()
        loan = {
            "id": state["next_id"],
            "item": "mic",
            "quantity": 1,
            "status": "returned",
        }
        state["loans"].append(loan)

        before_count = state["stock"]["mic"]
        result = return_loan(state, loan["id"])
        self.assertEqual(before_count, state["stock"]["mic"])

    def test_return_returned_loan_light(self):
        state = new_state()
        loan = {
            "id": state["next_id"],
            "item": "light",
            "quantity": 1,
            "status": "returned",
        }
        state["loans"].append(loan)

        before_count = state["stock"]["light"]
        result = return_loan(state, loan["id"])
        self.assertEqual(before_count, state["stock"]["light"])

    def test_return_loan_id_two(self):
        state = new_state()
        issue(state, "mic", "1")
        before_count = state["stock"]["mic"]
        issue(state, "mic", "1")
        result = return_loan(state, 2)
        self.assertEqual(before_count, state["stock"]["mic"])

    def test_return_loan_id_three(self):
        state = new_state()
        issue(state, "mic", "1")
        issue(state, "mic", "1")
        before_count = state["stock"]["mic"]
        issue(state, "mic", "1")
        result = return_loan(state, 3)
        self.assertEqual(before_count, state["stock"]["mic"])
