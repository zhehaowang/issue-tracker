#!/usr/bin/env python3

import unittest
from review import Review
from datetime import datetime

class TestReview(unittest.TestCase):
    def setUp(self):
        return

    def test_review_simple(self):
        r = Review()
        daily = {
            '08/31/18': {
                'date': datetime(year = 2018, month = 8, day = 31),
                'item': 'it 4'
            },
            '08/30/18': {
                'date': datetime(year = 2018, month = 8, day = 30),
                'item': 'it 1; it 2, it3'
            },
        }
        conf = {
            'review-1': '24',
            'review-2': '72',
            'review-3': '168',
            'max-review-items': '1'
        }
        reviews = {}
        r.merge_review_items(daily, conf, reviews)
        self.assertEqual(r.reschedule_and_generate_todo(conf, reviews),  ['it 1'], "Expect 1st item from day1")

if __name__ == '__main__':
    unittest.main()
