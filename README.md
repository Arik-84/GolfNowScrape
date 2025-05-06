# GolfNowScrape
A selenium/bs4 based auto scraper retrieving all available golf courses in a user’s area for a selected date from GolfNow, including full tee time availability, pricing, and address. LETS GO GOLFING!

Features
User inputs location and date

Scrapes all golf courses in the area from GolfNow for that day

Extracts:

Course name

All available tee times

Price per tee time

Course address

Saves results to a CSV for easy filtering and comparison

Tech Stack
Python 3

Selenium

pandas

bs4

Getting Started
1. Clone This Repo
bash
Copy
Edit
git clone https://github.com/your-username/golfnow-scraper.git
cd golfnow-scraper
2. Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
If not included, requirements.txt should contain:

nginx
Copy
Edit
selenium
pandas
3. Set Up ChromeDriver
Make sure ChromeDriver matches your Chrome version and is in your system PATH.
Download here

4. Run the Script
bash
Copy
Edit
python golfnow_scraper.py
You’ll be prompted to enter:

Location (e.g., "Toronto")

Date (e.g., "2025-05-07")

5. Output
The script saves a file named like:

Copy
Edit
golf_results_Toronto_2025-05-07.csv
Containing:

Course Name	Tee Time	Price	Address
Don Valley GC	8:30 AM	$65	4200 Yonge St, Toronto...

Project Structure
php-template
Copy
Edit
golfnow-scraper/
├── golfnow_scraper.py
├── README.md
├── requirements.txt
└── golf_results_<location>_<date>.csv
📄 License
This project is licensed under the MIT License.

Would you like me to also generate a requirements.txt file or example output CSV?







