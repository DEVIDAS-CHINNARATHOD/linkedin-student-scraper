import csv
import os
import time
from serpapi import GoogleSearch
from dotenv import load_dotenv

# ===== LOAD ENV KEYS =====
load_dotenv()
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

if not SERPAPI_KEY:
    raise EnvironmentError(
        "SERPAPI_KEY not found. Please set it in .env file or environment variables."
    )


def extract_name(title: str) -> str:
    """
    Extract name from LinkedIn title safely.
    Examples:
    - John Doe - Student at XYZ
    - John Doe | LinkedIn
    """
    if not title:
        return ""

    separators = [" - ", " | "]
    for sep in separators:
        if sep in title:
            return title.split(sep)[0].strip()

    return title.strip()


def fetch_students(college_name: str, batch_size: int = 10, max_results: int = 50):
    """
    Fetch student LinkedIn profiles using SerpAPI with deduplication
    and error handling.
    """
    students = []
    seen_links = set()
    empty_batches = 0

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

        try:
            search = GoogleSearch(params)
            results = search.get_dict()
        except Exception as e:
            print(f"[!] API error at start={start}: {e}")
            break

        organic_results = results.get("organic_results", [])

        if not organic_results:
            empty_batches += 1
            if empty_batches >= 2:
                print("[!] No new results. Stopping early.")
                break
            continue

        new_data_found = False

        for res in organic_results:
            link = res.get("link", "").strip()
            title = res.get("title", "").strip()
            name = extract_name(title)

            if link and name and link not in seen_links:
                seen_links.add(link)
                students.append({
                    "name": name,
                    "linkedin": link
                })
                new_data_found = True

        if not new_data_found:
            empty_batches += 1
            if empty_batches >= 2:
                print("[!] Duplicate-only batches detected. Stopping.")
                break
        else:
            empty_batches = 0

        # Respect rate limits
        time.sleep(1.2)

    return students


def save_to_csv(students, filename="students.csv"):
    """Save students list to CSV safely."""
    if not students:
        print("[!] No data to save.")
        return

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "linkedin"])
        writer.writeheader()
        writer.writerows(students)


if __name__ == "__main__":
    college_name = input("Enter college name: ").strip()

    if not college_name:
        print("[!] College name cannot be empty.")
        exit(1)

    students = fetch_students(college_name, batch_size=5, max_results=50)
    save_to_csv(students)

    print(f"[✔] Saved {len(students)} unique results to students.csv")
