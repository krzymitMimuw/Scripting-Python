import argparse
from pathlib import Path
from json_data import read_json, write_json

def write_csv(filepath):
    raise NotImplementedError("CSV writing must be implemented by person 1/3")

def read_csv(filepath):
    raise NotImplementedError("CSV reading must be implemented by person 1/3")

months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

days_of_the_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
day_intervals = []
for i in range(7):
    for j in range(i+1, 7):
        day_intervals.append(days_of_the_week[i] + "-" + days_of_the_week[j])

for x in days_of_the_week:
    day_intervals.append(x)

parts_of_the_day = ["Morning", "Evening"]

parser = argparse.ArgumentParser(description="File manager")

parser.add_argument("-m", "--months", nargs="*", type=str.title, choices=months, help="months (default: all)")
parser.add_argument("-d", "--days", nargs="*", type=str.title, choices=day_intervals, help="intervals of days of the week (default: Monday-Sunday)")
parser.add_argument("-p", "--periods", nargs="*", type=str.title, choices=parts_of_the_day, default=["Morning"], help="parts of the days (default: %(default)s)")

group_read_write = parser.add_mutually_exclusive_group()
group_read_write.add_argument("-t", "--write", action="store_true", help="write data to given place")
group_read_write.add_argument("-o", "--read", action="store_true", help="read data of given place")

group_csv_json = parser.add_mutually_exclusive_group()
group_csv_json.add_argument("-c", "--csv", action="store_true", help="create/export as csv")
group_csv_json.add_argument("-j", "--json", action="store_true", help="create/export as json")

parser.add_argument("-r", "--root", default=".", help="root directory for the Month/Day/Period tree (default: %(default)s)")

def get_days(interval):
    if "-" in interval:
        start, end = interval.split("-")
        start_idx = days_of_the_week.index(start)
        end_idx = days_of_the_week.index(end)
        return days_of_the_week[start_idx : end_idx + 1]
    else:
        return [interval]


def generate_paths(root, selected_months=None, selected_days=None, periods=None):
    """Return unique Month/Day/Period paths without creating directories.

    Months and day intervals are paired. Missing values mean all months and
    Monday-Sunday. Periods apply to expanded days in order, then default to Morning.
    """
    months_args = selected_months or months
    days_args = selected_days or ["Monday-Sunday"] * len(months_args)
    periods_args = periods or []
    if len(months_args) != len(days_args):
        raise ValueError("Number of months must be the same as number of day-intervals!")
    if any(month not in months for month in months_args):
        raise ValueError("Unknown month")
    if any(interval not in day_intervals for interval in days_args):
        raise ValueError("Unknown day or invalid day interval")
    if any(period not in parts_of_the_day for period in periods_args):
        raise ValueError("Unknown part of the day")

    result = []
    for month, interval in zip(months_args, days_args):
        days = get_days(interval)
        for day in days:
            result.append((month, day))
    
    paths = []
    for i, (month, day) in enumerate(result):
        period = periods_args[i] if i < len(periods_args) else "Morning"
        paths.append(Path(root) / month / day / period)
    return list(dict.fromkeys(paths))


def manage_files(args):
    paths = generate_paths(args.root, args.months, args.days, args.periods)
    read_time = 0
    for directory in paths:
        if args.write:
            directory.mkdir(parents = True, exist_ok = True)
            print(f"Created directory: {directory}")
            if args.csv:
                path = directory / "Dane.csv"
                write_csv(path)
            elif args.json:
                path = directory / "Dane.json"
                write_json(directory)
        elif args.read:
            if not directory.exists():
                print(f"Path: {directory} doesn't exists")
                continue
            if args.csv:
                path = directory / "Dane.csv"
                if path.exists():
                    read_time += read_csv(path)
                else:
                    print(f"No such file as {path}")
            elif args.json:
                path = directory / "Dane.json"
                if path.exists():
                    read_time += read_json(directory)
                else:
                    print(f"No such file as {path}")

    if args.read:
        print(f"Total Czas for Model A: {read_time}s")
    return read_time
    
if __name__ == "__main__":
    args = parser.parse_args()
    try:
        manage_files(args)
    except (ValueError, NotImplementedError) as exc:
        parser.error(str(exc))
