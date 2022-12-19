class Moment(object):

    def __init__(self, year: int = 1, month: int = 1, day: int = 1, hour: int = 0, minute: int = 0, second: int = 0) -> None:

        self.year = Year(year)
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.second = second

        self._verify()

    def _verify(self) -> None:

        assert type(self.month) == int, "Month must be an integer"
        assert type(self.day) == int, "Day must be an integer"
        assert type(self.hour) == int, "Hour must be an integer"
        assert type(self.minute) == int, "Minute must be an integer"
        assert type(self.second) == int, "Second must be an integer"

        assert self.month > 0 and self.month < 13, "Month must be in between 1 to 12 including both ends"

        assert self.day > 0 and self.day <= self.year.month_days[self.month], f"Day must be in between 1 to {self.year.month_days[self.month]}"

        assert self.hour >= 0 and self.hour <= 23, "Hour must be in between 0 to 23"
        assert self.minute >= 0 and self.minute <= 59, "Minute must be in between 0 to 59"
        assert self.second >= 0 and self.second <= 59, "Second must be in between 0 to 59"

    def __sub__(self, other: "Moment") -> int:

        if self.year.year == other.year.year:
            return other._days_to_end() - self._days_to_end()
        elif self.year.year == other.year.year+1:
            return other._days_to_end() + self._days_to_date()
        else:
            days = other._days_to_end() + self._days_to_date()
            days += sum([Year(int(year)).day_count for year in range(other.year.year+1, self.year.year)])
            return days

    def __str__(self) -> str:
        s = f"{self.month}/{self.day}/{self.year}, {self.hour}:{self.minute}:{self.second}"
        return s

    def _days_to_date(self) -> int:
        days = 0
        for i in range(1, self.month):
            days += self.year.month_days[i]

        days += self.day
        return days

    def _days_to_end(self) -> int:
        return self.year.day_count - self._days_to_date()


class Year(object):

    def __init__(self, year: int = 1) -> None:
        self.year = year
        self._verify()

        self.leap = self._leap_year()

        self.day_count = 365 + self.leap
        self.month_days = {1: 31, 2: 28+self.leap, 3: 31, 4: 30,
                           5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}

    def _verify(self) -> None:
        assert type(self.year) == int, "Year must be an integer"
        assert self.year > 0, "Year must be positive"

    def _leap_year(self) -> bool:
        return Year._check_leap(self.year)

    @staticmethod
    def _check_leap(year: int) -> bool:
        div4 = year % 4 == 0
        div100 = year % 100 == 0
        div400 = year % 400 == 0
        div4000 = year % 4000 == 0

        if div4000:
            return False
        elif div100:
            if div400:
                return True
            return False
        elif div4:
            return True
        else:
            return False

    def __str__(self) -> str:
        return f"{self.year}"


def main() -> None:

    # List of tuples for the time interval outside of the US, first date is for departure, second one is for arrival
    outside_US = [(Moment(2017, 10, 1), Moment(2017, 12, 16)),  # Scholarship
                  (Moment(2017, 12, 16), Moment(2018, 1, 10)),  # Turkey trip
                  (Moment(2018, 6, 18), Moment(2018, 7, 23)),  # Turkey trip
                  (Moment(2018, 12, 15), Moment(2019, 1, 9)),  # Turkey trip
                  (Moment(2019, 6, 11), Moment(2019, 7, 10)),  # Turkey trip
                  (Moment(2019, 12, 17), Moment(2020, 1, 3)),  # Turkey trip
                  (Moment(2020, 11, 8), Moment(2020, 12, 30)),  # Turkey trip
                  (Moment(2021, 6, 14), Moment(2021, 9, 17)),  # Internship
                  (Moment(2021, 9, 23), Moment(2021, 10, 28))]  # Turkey trip

    interval = 0
    for out in outside_US:
        interval += out[1]-out[0]

    # Today's date - Starting date for your work
    total_days = Moment(2021, 12, 8) - Moment(2017, 10, 1)

    print(f"Cumulative number of days: \t {total_days}")
    print(f"Total working days in the US: \t {total_days - interval}")
    print(f"Total days needed for waiver: \t {365*3}")
    print(f"Remaining days to finish: \t {max(365*3-(total_days - interval), 0)}")


if __name__ == '__main__':
    main()
