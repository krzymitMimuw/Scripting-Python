import argparse

months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

days_of_the_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
day_intervals = []
for i in range(7):
    for j in range(i+1, 7):
        day_intervals.append(days_of_the_week[i] + "-" + days_of_the_week[j])

for x in days_of_the_week:
    days_intervals.append(x)

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
args = parser.parse_args()




