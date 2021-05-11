
import collections
import datetime
import glob
import utmp

MONTHS = {
    'jan': 1,
    'feb': 2,
    'mar': 3,
    'apr': 4,
    'may': 5,
    'jun': 6,
    'jul': 7,
    'aug': 8,
    'sep': 9,
    'oct': 10,
    'nov': 11,
    'dec': 12
}

DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']


class FakeEntry:
    def __init__(self, time, user):
        self.time = time
        self.user = user


def main():
    entries = []
    for fn in glob.glob('/var/log/wtmp*'):
        with open(fn, 'rb') as fd:
            for entry in utmp.read(fd.read()):
                if entry.user in ['reboot', 'shutdown']:
                    entries.append(entry)

    entries.sort(key=lambda x: x.time)

    now = datetime.datetime.now()
    entries.append(FakeEntry(now, 'shutdown'))

    time_by_day = collections.defaultdict(datetime.timedelta)
    time_by_week = collections.defaultdict(datetime.timedelta)

    last_reboot = None
    for entry in entries:
        if entry.user == 'shutdown' and last_reboot:
            year, week, day = last_reboot.isocalendar()
            delta = entry.time - last_reboot
            time_by_day[(year, week, day)] += delta
            time_by_week[(year, week)] += delta
            last_reboot = None
        elif entry.user == 'reboot':
            last_reboot = entry.time

    for key, delta in sorted(time_by_day.items()):
        hours = delta.total_seconds() / 3600
        year, week, day = key
        print('{} {:>2} {}'.format(year, week, day), '{:<10}'.format(DAYS[key[-1]-1]), '{:>7.2f}'.format(hours))

    for key, delta in sorted(time_by_week.items()):
        hours = delta.total_seconds() / 3600
        year, week = key
        print('{} {:>2}'.format(year, week), '{:>7.2f}'.format(hours))

if __name__ == '__main__':
    main()
