import datetime
import time
from itertools import cycle
from typing import List


class IntervalCollector:
    """
    Given a list of scraper objects, perform different data collection tasks
    """

    def __init__(self, scrapers: List["Scrapers"]) -> None:
        if not type(scrapers) == list:
            scrapers = list(scrapers)
        self.scrapers = scrapers

    def _calculate_time_remaining(self, current, end):
        return (end - current).seconds

    def interval_scrape(
        self,
        min_interval: int = 5,
        days: int = 0,
        seconds: int = 60,
        microseconds: int = 0,
        milliseconds: int = 0,
        minutes: int = 0,
        hours: int = 0,
        weeks: int = 0,
        quiet: bool = False,
    ):

        current_time = datetime.datetime.now()
        end_time = current_time + datetime.timedelta(
            days=days,
            seconds=seconds,
            microseconds=microseconds,
            milliseconds=milliseconds,
            minutes=minutes,
            hours=hours,
            weeks=weeks,
        )

        # TODO: Process list asynchronously and then wait so that each
        # scraper is processed at basically the same time before waiting

        # Wait during interval, scrape data, then check if current time has passed end time
        if not quiet:
            print(f"Starting scrape, {self._calculate_time_remaining(current_time, end_time)} seconds remaining")
        for scraper in cycle(self.scrapers):
            time.sleep(min_interval)
            scraper.static_load()
            current_time = datetime.datetime.now()
            time_remaining = self._calculate_time_remaining(current_time, end_time)
            if not quiet:
                if time_remaining > 0:
                    print(f"{scraper} scraped: {time_remaining} seconds remaining")
                else:
                    print(f"{scraper} scraped: No time remaining, exitting")
            if current_time > end_time or time_remaining < min_interval:
                break


class IntervalIterator(IntervalCollector):
    """
    Iterator for scraping at given intervals
    """

    def __init__(
        self,
        scrapers,
        min_interval: int = 5,
        days: int = 0,
        seconds: int = 60,
        microseconds: int = 0,
        milliseconds: int = 0,
        minutes: int = 0,
        hours: int = 0,
        weeks: int = 0,
        quiet: bool = False,
    ):
        self.scrapers = scrapers
        self.min_interval = min_interval
        self.days = days
        self.seconds = seconds
        self.microseconds = microseconds
        self.milliseconds = milliseconds
        self.minutes = minutes
        self.hours = hours
        self.weeks = weeks
        self.quiet = quiet
        self.current = self.scrapers[0]
        self.scrapers = cycle(self.scrapers)

        self.current_time = datetime.datetime.now()
        self.end_time = self.current_time + datetime.timedelta(
            days=days,
            seconds=seconds,
            microseconds=microseconds,
            milliseconds=milliseconds,
            minutes=minutes,
            hours=hours,
            weeks=weeks,
        )
        if not self.quiet:
            print(
                f"Starting scrape, {self._calculate_time_remaining(self.current_time, self.end_time)} seconds remaining"
            )

    def __iter__(self):
        return self

    def __next__(self, val=True):

        time.sleep(self.min_interval)
        self.current.static_load()
        self.current_time = datetime.datetime.now()
        self.time_remaining = self._calculate_time_remaining(self.current_time, self.end_time)
        if not self.quiet:
            if self.time_remaining > 0:
                print(f"{self.current} scraped: {self.time_remaining} seconds remaining")
            else:
                print(f"{self.current} scraped: No time remaining, exitting")
        self.current = next(self.scrapers)
        if self.current_time > self.end_time or self.time_remaining < self.min_interval:
            raise StopIteration
