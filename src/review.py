#!/usr/bin/env python3

from datetime import datetime, timedelta

class Review():
    def __init__(self):
        self.MAX_REVIEW_ITEM_CNT = 3
        return

    def merge_review_items(self, daily, confs, reviews):
        review_schedule = []
        for i in range(1, 6):
            key = 'review-' + str(i)
            if key in confs:
                review_schedule.append(int(confs[key]))

        candidate_items = []
        sorted_daily = sorted(daily, key = lambda x : daily[x]['date'])
        for entry in sorted_daily:
            items = daily[entry]['item'].split(';')
            for item in items:
                key = item.strip()
                start_time = datetime.now()
                if key:
                    if key in reviews:
                        # update review dates of review-n that is not done yet
                        offset = 0
                        for r in reviews[key]:
                            if r["status"] != "done":
                                projected_time = start_time + timedelta(hours = review_schedule[offset])
                                if r["time"] < projected_time:
                                    r["time"] = projected_time
                                    r["reschedule_cnt"] += 1
                                    # rescheduled items get a higher priority
                                    candidate_items.insert(0, key)
                            offset += 1
                    else:
                        # write scheduled review dates, starting from today
                        reviews[key] = []
                        for hour in review_schedule:
                            event = {
                                "status": "scheuduled",
                                "time": start_time + timedelta(hours = hour),
                                "reschedule_cnt": 0
                            }
                            reviews[key].append(event)
                            if hour <= 24:
                                candidate_items.append(key)

        max_review_items = self.MAX_REVIEW_ITEM_CNT
        if 'max-review-items' in confs:
            max_review_items = int(confs['max-review-items'])

        return candidate_items[:max_review_items]