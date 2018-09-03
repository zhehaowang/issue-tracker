#!/usr/bin/env python3

import random
from datetime import datetime, timedelta

"""
Main business logic class
"""

class Review():
    def __init__(self):
        self.MAX_REVIEW_ITEM_CNT = 3
        return

    """
    Given a configuration dictionary, generate a list of review schedules.

    @param  dict <configuration key, configuration value>
    @return [int], where each element is the number of hours to next review
    """
    def get_review_schedule(self, confs):
        review_schedule = []
        for i in range(1, 6):
            key = 'review-' + str(i)
            if key in confs:
                review_schedule.append(int(confs[key]))
        return review_schedule

    """
    Fill review dates in reviews object. Use this when the given review dict
    may contain less entries than the number of scheduled reviews. (e.g. manually
    added items to review_backlog without going through daily).

    @param  dict <configuration key, configuration value>
    @param  dict <review item, {status: str, time: datetime, reschedule_cnt: int}>,
            modified in-place
    @return None
    """
    def fill_review_dates(self, confs, reviews):
        review_schedule = self.get_review_schedule(confs)
        start_time = datetime.now()
        
        for key in reviews:
            for idx in range(len(reviews[key]), len(review_schedule)):
                event = {
                    "status": "scheduled",
                    "time": start_time + timedelta(hours = review_schedule[idx]),
                    "reschedule_cnt": 0
                }
                reviews[key].append(event)
        return

    """
    Merge the items in review and items read from daily. Ignore the items in daily
    that are already in review.

    @param  dict <date, {items: str}>
    @param  dict <configuration key, configuration value>
    @param  dict <review item, {status: str, time: datetime, reschedule_cnt: int}>,
            modified in-place
    @return None
    """
    def merge_review_items(self, daily, confs, reviews):
        review_schedule = self.get_review_schedule(confs)
        start_time = datetime.now()

        for entry in daily:
            items = daily[entry]['item'].split(';')
            for item in items:
                key = item.strip()
                if key:
                    if not key in reviews:
                        # write scheduled review dates, starting from today
                        reviews[key] = []
                        for hour in review_schedule:
                            event = {
                                "status": "scheduled",
                                "time": start_time + timedelta(hours = hour),
                                "reschedule_cnt": 0
                            }
                            reviews[key].append(event)
        return

    """
    Given a merged view of review items, reschedule items whereas needed and
    generate a todo list up to the number of configured daily review items.

    @param  dict <configuration key, configuration value>
    @param  dict <review item, {status: str, time: datetime, reschedule_cnt: int}>
    @return [str]
    """
    def reschedule_and_generate_todo(self, confs, reviews):
        review_schedule = self.get_review_schedule(confs)
        start_time = datetime.now()
        candidate_items = []

        # update review dates of review-n that is not done yet
        for key in reviews:
            offset = 0
            reschedule_cnt_incremented = False
            for r in reviews[key]:
                if r["status"] != "done":
                    projected_time = start_time + timedelta(hours = review_schedule[offset])
                    if r["time"] < projected_time:
                        r["time"] = projected_time
                        if not reschedule_cnt_incremented:
                            r["reschedule_cnt"] += 1
                            reschedule_cnt_incremented = True
                        # rescheduled items get a higher priority
                offset += 1
            candidate_items.append(key)

        max_review_items = self.MAX_REVIEW_ITEM_CNT
        if 'max-review-items' in confs:
            max_review_items = int(confs['max-review-items'])

        random.shuffle(candidate_items)
        return candidate_items[:max_review_items]

    def serialize_single_event(self, event):
        return event['time'].strftime('%m/%d/%y') + '; ' + str(event['status']) + '; ' + str(event['reschedule_cnt'])

    """
    Given a merged view of review items, convert it to array of arrays ready for
    writing back to sheet.

    @param  dict <review item, {status: str, time: datetime, reschedule_cnt: int}>
    @return [[str]]
    """
    def to_table(self, reviews):
        content = [['Items', 'Review-1', 'Review-2', 'Review-3', 'Review-4', 'Review-5']]
        for key in reviews:
            row = [key]
            row += [self.serialize_single_event(x) for x in reviews[key]]
            content.append(row)
        return content
