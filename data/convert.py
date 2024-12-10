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

# Regex patterns to detect and parse date/time
# Examples of formats we might encounter:
# "Utlevering: 19. november 2024 kl. 09:00"
# "Innlevering: 21. november 2024 kl. 13:00"
# "Dato: 12. desember 2024 kl. 09:00"
# "Fra 3. desember  til 5. desember 2024"
# We'll try to handle these cases.

date_time_pattern = re.compile(
    r'(?P<day>\d{1,2})\.\s*(?P<month>\w+)\s+(?P<year>\d{4})\s*(kl\.\s*(?P<hour>\d{1,2}):(?P<minute>\d{2}))?'
)

date_range_pattern = re.compile(
    r'Fra\s+(?P<start_day>\d{1,2})\.\s*(?P<start_month>\w+)\s*(til\s+(?P<end_day>\d{1,2})\.\s*(?P<end_month>\w+))?\s+(?P<year>\d{4})'
)

single_date_pattern = re.compile(
    r'Dato:\s*(?P<day>\d{1,2})\.\s*(?P<month>\w+)\s+(?P<year>\d{4})\s*(kl\.\s*(?P<hour>\d{1,2}):(?P<minute>\d{2}))?'
)

# Helper functions

def parse_datetime(day, month, year, hour=None, minute=None):
    day = int(day)
    m = month_map.get(month.lower(), None)
    if not m:
        return None
    if hour is None:
        hour = '00'
    if minute is None:
        minute = '00'
    try:
        dt = datetime(int(year), int(m), day, int(hour), int(minute), 0)
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    except ValueError:
        return None

def parse_date_line(date_str):
    # Attempt to parse multiple date entries (e.g., Utlevering and Innlevering)
    # Split by line break first, then parse each line
    parts = date_str.split('\n')
    parts = [p.strip() for p in parts if p.strip()]

    # We'll store parsed datetimes in a list
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
            if start_dt and end_dt:
                datetimes.append(f'{start_dt} to {end_dt}')
            elif start_dt:
                datetimes.append(start_dt)
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

    # If we parsed multiple datetime entries, join them with ' to ' if there are two.
    # If more than two, we just join them with semicolons.
    if len(datetimes) == 2 and ' to ' not in datetimes[0]:
        # If exactly two timestamps, join with " to "
        return f'{datetimes[0]} to {datetimes[1]}'
    elif len(datetimes) > 2:
        # Join all with semicolons
        return '; '.join(datetimes)
    elif len(datetimes) == 1:
        return datetimes[0]
    else:
        # Could not parse, return original string (without line breaks)
        return ' '.join(parts)

# Main code
input_file = 'allcombined.csv'   # Change to your actual input file
output_file = 'output.csv' # Change to your desired output file

with open(input_file, 'r', newline='', encoding='utf-8') as infile, \
     open(output_file, 'w', newline='', encoding='utf-8') as outfile:

    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    header = next(reader)

    # Original headers: Course Code,Exam Type,Date(s),Room Info
    # Replace with supabase-compatible headers
    # Lowercase, underscores, no parentheses in header names:
    new_header = ["course_code", "exam_type", "dates", "room_info"]
    writer.writerow(new_header)

    for row in reader:
        if len(row) < 4:
            continue
        course_code = row[0]
        exam_type = row[1]
        dates_str = row[2]
        room_info = row[3]

        # Parse and convert the dates_str
        converted_dates = parse_date_line(dates_str)

        writer.writerow([course_code, exam_type.replace(' ', '_'), converted_dates, room_info])
