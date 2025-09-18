# 🎓 LinkedIn Student Scraper

A Python script to scrape **LinkedIn student/alumni profiles** of a given college using [SerpApi](https://serpapi.com/).  
It saves the results into a **CSV file** with names and LinkedIn profile links.

---

## 🚀 Features

- Fetch LinkedIn profiles of students/alumni from a given college.
- Automatically handles batch fetching and saves results into CSV.
- Simple CLI interface.
- Uses SerpApi (Google Search API).

---

## 📂 Project Structure
```
linkedin-student-scraper/
│── main.py 
│── requirements.txt 
│── .env.example 
│── README.md 
```
---

## ⚙️ Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/linkedin-student-scraper.git
cd linkedin-student-scraper
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate     # On Linux/Mac
venv\Scripts\activate      # On Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
- Copy `.env.example` → `.env`
- Add your **SerpApi key** inside `.env`

```
SERPAPI_KEY=your_serpapi_key_here
```

### 5. Run the Script
```bash
python main.py
```

---

## 🛠 Requirements
- Python 3.8+
- SerpApi Key
