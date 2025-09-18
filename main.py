import csv
import os
import time
from serpapi import GoogleSearch
from dotenv import load_dotenv

# ===== LOAD ENV KEYS =====
load_dotenv()
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

def fetch_students(college_name: str, batch_size: int = 10, max_results: int = 50):
    """
    Fetch student LinkedIn profiles in batches from SerpApi.
    
    Args:
        college_name (str): The college/university name to search for.
        batch_size (int): Number of results per API call.
        max_results (int): Total results to fetch.
    
    Returns:
        list[dict]: List of dictionaries with name and LinkedIn profile.
    """
    all_students = []

    for start in range(0, max_results, batch_size):
        query = (
            f'site:linkedin.com/in "{college_name}" '
            f'(alumni OR student OR graduate OR studied) '
            f'-professor -lecturer -faculty -teacher'
        )

        params = {
            "q": query,
            "hl": "en",
            "gl": "in",
            "num": batch_size,
            "start": start,
            "api_key": SERPAPI_KEY
        }

        search = GoogleSearch(params)
        results = search.get_dict()

        for res in results.get("organic_results", []):
            title = res.get("title", "")
            link = res.get("link", "")
            name = title.split(" - ")[0].strip() if title else ""
            if name and link:
                all_students.append({
                    "name": name,
                    "linkedin": link
                })

        # Avoid rate limiting
        time.sleep(1)

    return all_students

def save_to_csv(students, filename="students.csv"):
    """Save list of students to a CSV file."""
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "linkedin"])
        writer.writeheader()
        writer.writerows(students)

if __name__ == "__main__":
    college_name = input("Enter college name: ").strip()
    students = fetch_students(college_name, batch_size=5, max_results=50)
    save_to_csv(students)
    print(f"[✔] Saved {len(students)} results to students.csv")
