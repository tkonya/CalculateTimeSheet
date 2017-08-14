import datetime
import math

per_hour = 100
time_tracking_file = open('filename', 'rb+')
time_format = '%I:%M%p'

read_list = time_tracking_file.read().splitlines()
write_list = []

time_tracking_file.close()

current_day = ''
day_total_hours = 0

second = 'xxx'
third = 'xxx'

in_at = None
out_at = None

for index, line in enumerate(read_list):

    line = line.decode('UTF-8').strip()

    print('\n---------------\nlooking at ' + line)

    first = second
    second = third
    third = line

    if in_at is not None and out_at is not None:
        print('calculating time difference')
        diff = out_at - in_at

        hours = diff.seconds / 3600
        day_total_hours += hours
        expected_pay = float(hours) * per_hour

        print(str(in_at.time()) + ' through ' + str(out_at.time()) + ': ' + str(math.ceil(hours * 100) / 100))

        new_line = '\n( ' + str(math.ceil(hours * 100) / 100) + ' hours worked / $' + \
                   str(math.ceil(expected_pay * 100) / 100) + ' estimated pay )'

        if line.strip() == '' or 'estimated pay' in line:
            write_list.append(new_line)
        else:
            write_list.append(new_line + '\n' + line)

        in_at = None
        out_at = None

    elif day_total_hours > 0 and (line.strip() == '' or 'hours worked total' in line or 'day total' in line):
        print('calculating day total')
        if day_total_hours != 0 and current_day != '':
            expected_pay = float(day_total_hours) * per_hour
            write_list.append('\n( ' +
                              str(math.ceil(day_total_hours * 100) / 100) + ' hours worked total / $' + str(math.ceil(expected_pay * 100) / 100) + ' estimated pay total )\n')
            day_total_hours = 0
            current_day = ''

    elif line.startswith('2017') or line.startswith('2018') or line.startswith('2019'):
        print('this line is a new day')
        current_day = line

        if len(write_list) == 0:
            write_list.append(line)
        elif write_list[len(write_list) - 1].strip() != '':
            write_list.append('\n\n' + line)
        else:
            write_list.append(line)

    else:
        print('just writing a normal line')
        write_list.append('\n' + line)

    if line.startswith('in at'):
        in_at = datetime.datetime.strptime(line.replace('in at ', '').strip(), time_format)
        print('setting in at: ' + str(in_at))
    elif line.startswith('out at'):
        out_at = datetime.datetime.strptime(line.replace('out at ', '').strip(), time_format)
        print('setting out at: ' + str(out_at))

# write things
time_tracking_file = open('filename', 'w')
for line in write_list:
    time_tracking_file.write(line)

time_tracking_file.close()
