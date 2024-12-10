import csv
import re
from datetime import datetime

# Norwegian month mapping
month_map = {
    'januar': '01',
    'februar': '02',
    'mars': '03',
    'april': '04',
    'mai': '05',
    'juni': '06',
    'juli': '07',
    'august': '08',
    'september': '09',
    'oktober': '10',
    'november': '11',
    'desember': '12'
}

# Regex patterns for parsing dates
date_time_pattern = re.compile(
    r'(?P<day>\d{1,2})\.\s*(?P<month>\w+)\s+(?P<year>\d{4})\s*(kl\.\s*(?P<hour>\d{1,2}):(?P<minute>\d{2}))?'
)

date_range_pattern = re.compile(
    r'Fra\s+(?P<start_day>\d{1,2})\.\s*(?P<start_month>\w+)\s*(til\s+(?P<end_day>\d{1,2})\.\s*(?P<end_month>\w+))?\s+(?P<year>\d{4})'
)

single_date_pattern = re.compile(
    r'Dato:\s*(?P<day>\d{1,2})\.\s*(?P<month>\w+)\s+(?P<year>\d{4})\s*(kl\.\s*(?P<hour>\d{1,2}):(?P<minute>\d{2}))?'
)

def parse_datetime(day, month, year, hour=None, minute=None):
    m = month_map.get(month.lower(), None)
    if not m:
        return None
    if hour is None:
        hour = '00'
    if minute is None:
        minute = '00'
    try:
        dt = datetime(int(year), int(m), int(day), int(hour), int(minute), 0)
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    except ValueError:
        return None

def parse_date_line(date_str):
    # This function now returns a list of parsed datetimes.
    parts = date_str.split('\n')
    parts = [p.strip() for p in parts if p.strip()]
    datetimes = []

    for part in parts:
        # Check if it's a range
        range_match = date_range_pattern.search(part)
        if range_match:
            start_day = range_match.group('start_day')
            start_month = range_match.group('start_month')
            end_day = range_match.group('end_day')
            end_month = range_match.group('end_month')
            year = range_match.group('year')

            # If only one month is given, assume end_month = start_month
            if not end_month:
                end_month = start_month

            start_dt = parse_datetime(start_day, start_month, year)
            end_dt = parse_datetime(end_day, end_month, year) if end_day else None
            if start_dt:
                datetimes.append(start_dt)
            if end_dt:
                datetimes.append(end_dt)
            continue

        # Check single date line format (Dato: ...)
        single_match = single_date_pattern.search(part)
        if single_match:
            day = single_match.group('day')
            month = single_match.group('month')
            year = single_match.group('year')
            hour = single_match.group('hour')
            minute = single_match.group('minute')
            dt = parse_datetime(day, month, year, hour, minute)
            if dt:
                datetimes.append(dt)
            continue

        # General date/time pattern (Utlevering/Innlevering)
        general_match = date_time_pattern.search(part)
        if general_match:
            day = general_match.group('day')
            month = general_match.group('month')
            year = general_match.group('year')
            hour = general_match.group('hour')
            minute = general_match.group('minute')
            dt = parse_datetime(day, month, year, hour, minute)
            if dt:
                datetimes.append(dt)
            continue

    return datetimes

def determine_start_end(datetimes):
    # Based on number of parsed datetimes, determine start_time and end_time
    if len(datetimes) == 0:
        return '', ''
    elif len(datetimes) == 1:
        return datetimes[0], ''
    else:
        # If more than one, start_time = first, end_time = last
        return datetimes[0], datetimes[-1]

input_file = 'allcombined.csv'   # Change to your actual input file
output_file = 'output.csv' # Change to your desired output file

with open(input_file, 'r', newline='', encoding='utf-8') as infile, \
     open(output_file, 'w', newline='', encoding='utf-8') as outfile:

    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    # Write new header
    # course_code,exam_type,start_time,end_time,location
    writer.writerow(["course_code", "exam_type", "start_time", "end_time", "location"])

    header = next(reader)  # skip original header

    for row in reader:
        if len(row) < 4:
            continue
        course_code = row[0]
        exam_type = row[1]
        dates_str = row[2]
        location = row[3]

        # Parse the date line
        datetimes = parse_date_line(dates_str)
        start_time, end_time = determine_start_end(datetimes)

        # Replace spaces in exam_type with underscore if needed
        exam_type_fixed = exam_type.replace(' ', '_')

        writer.writerow([course_code, exam_type_fixed, start_time, end_time, location])
