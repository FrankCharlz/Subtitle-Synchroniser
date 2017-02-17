from datetime import datetime as dt
from datetime import timedelta

__author__ = 'Frank'

MINIMUM_TIME = dt.strptime('00:00:00,000', '%H:%M:%S,%f')

in_file_name = 'test.srt'
out_file_name = 'out_' + in_file_name

h = 0
m = 1
s = 0
diff = 3600 * h + 60 * m + s  # difference in seconds

direction = -1  # add time difference if 1, if -1 subtract
diff *= direction


def sync(line):
    # format of line: 00:06:28,081 --> 00:06:29,548
    parts = line.split('-->')

    start_time = dt.strptime(parts[0].strip(), '%H:%M:%S,%f')
    end_time = dt.strptime(parts[1].strip(), '%H:%M:%S,%f')

    start_time += timedelta(seconds=diff)
    end_time += timedelta(seconds=diff)

    if start_time < MINIMUM_TIME or end_time < MINIMUM_TIME: return line.strip()

    start_time = start_time.strftime('%H:%M:%S,%f')[0:-3]
    end_time = end_time.strftime('%H:%M:%S,%f')[0:-3]

    return start_time + ' --> ' + end_time

out = open(out_file_name, 'w')

with open(in_file_name, 'r') as lines:
    for line in lines:
        if '-->' in line:
            line = sync(line)
            out.write(line+'\n')
        else:
            out.write(line)


out.close()