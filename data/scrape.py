import csv
from bs4 import BeautifulSoup

# Path to your saved HTML file
html_file_path = "./eksamensdatoer_engineer_nt.html"  # Adjust the file path if needed

# Load the HTML source code from the file
with open(html_file_path, "r", encoding="utf-8") as file:
    html_content = file.read()

# Parse the HTML
soup = BeautifulSoup(html_content, 'html.parser')

# Find all exam cards
exam_cards = soup.find_all('div', class_='card well mb-3')

# Prepare data
data = []
for card in exam_cards:
    # Extract course code
    course_code = card.find('h5', class_='card-title')
    course_code = course_code.text.strip() if course_code else "N/A"
    
    # Extract exam type
    exam_type = card.find('h6', class_='card-subtitle')
    exam_type = exam_type.text.strip() if exam_type else "N/A"
    
    # Extract dates (can include multiple lines for multi-date exams)
    date_lines = card.find_all('div', string=lambda x: x and ('Dato:' in x or 'Utlevering:' in x or 'Innlevering:' in x or 'Fra' in x))
    dates_info = [line.string.strip() for line in date_lines]
    
    # Extract room info (if applicable)
    room_divs = card.find_all('div', class_='romListe py-2')
    room_info = "\n".join(div.text.strip() for div in room_divs) if room_divs else "N/A"
    
    # Append data
    data.append([course_code, exam_type, "\n".join(dates_info), room_info])

# Save to CSV
csv_file_path = "eksamensdatoer_nt_multiple.csv"
with open(csv_file_path, "w", encoding="utf-8", newline="") as csvfile:
    writer = csv.writer(csvfile)
    # Write the header
    writer.writerow(["Course Code", "Exam Type", "Date(s)", "Room Info"])
    # Write the data rows
    writer.writerows(data)

print(f"Data saved to {csv_file_path}")
