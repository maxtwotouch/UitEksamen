import csv
from bs4 import BeautifulSoup

# Path to your saved HTML file
html_file_path = "./eksamendatoer_kunst.html"  # Correctly use the path as a string

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
    
    # Extract date and time
    date_div = card.find('div', string=lambda x: x and x.startswith('Dato:'))
    date_info = date_div.string.strip().replace('Dato: ', '') if date_div else "N/A"
    
    # Extract room info
    room_div = card.find('div', class_='romListe py-2')
    room_info = room_div.text.strip() if room_div else "N/A"
    
    # Append data
    data.append([course_code, exam_type, date_info, room_info])

# Save to CSV
csv_file_path = "exam_data_kunst.csv"
with open(csv_file_path, "w", encoding="utf-8", newline="") as csvfile:
    writer = csv.writer(csvfile)
    # Write the header
    writer.writerow(["Course Code", "Exam Type", "Date & Time", "Room Info"])
    # Write the data rows
    writer.writerows(data)

print(f"Data saved to {csv_file_path}")
