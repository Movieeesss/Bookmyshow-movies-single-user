import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, timezone

# --- CONFIGURATION (UPDATE THESE IMMEDIATELY) ---
TOKEN = "8825463319:AAH285s09kaeYMTXsPCEd41gjiTA-GQbL7g"
CHAT_ID = "8095698350"
API_KEY = "e7f212ee-87d6-4800-b393-a5125808574c"

def get_trichy_movies():
    target_url = "https://in.bookmyshow.com/explore/movies-trichy"
    proxy_url = f"https://api.webscraping.ai/html?api_key={API_KEY}&url={target_url}&proxy=residential&render=true&wait=10000"
    
    movie_list = set() 
    try:
        print("Fetching data from BookMyShow...")
        response = requests.get(proxy_url, timeout=45)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Method 1: H3 tags check
            for h3 in soup.find_all('h3'):
                name = h3.get_text().strip().upper()
                if 2 < len(name) < 50:
                    blacklist = ["BOOKING", "TICKET", "WATCH", "CLICK", "OFFER", "LATEST", "BMS", "SCREEN"]
                    if not any(x in name for x in blacklist):
                        movie_list.add(name)

            # Method 2: Alt tags backup
            if not movie_list:
                for img in soup.find_all('img', alt=True):
                    name = img['alt'].strip().upper()
                    if 3 < len(name) < 45 and "LOGO" not in name and "BANNER" not in name:
                        movie_list.add(name)
            
            print(f"Scraped {len(movie_list)} movies.")
        else:
            print(f"Scraper Error: Status {response.status_code}")
            
    except Exception as e:
        print(f"Connection Error: {e}")
        
    return sorted(list(movie_list))

def run_all():
    movies = get_trichy_movies()
    
    ist_now = datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)
    time_str = ist_now.strftime("%d-%m-%Y | %I:%M %p")
    
    # Using HTML tags instead of Markdown to prevent parsing errors
    header = "🎬 <b>TRICHY MOVIES LIST</b> 🎬\n"
    meta = f"🕒 {time_str}\n━━━━━━━━━━━━━━━━━━━━\n"
    
    if not movies:
        body = "⚠️ <b>Status:</b> No movies detected. Check Proxy/API Key.\n"
    else:
        body = "🎥 <b>NOW SHOWING:</b>\n\n"
        for m in movies:
            # Clean up potential HTML-breaking characters in movie names
            clean_m = m.replace('<', '').replace('>', '').replace('&', 'and')
            body += f"✅ <b>{clean_m}</b>\n"
            
    footer = '\n━━━━━━━━━━━━━━━━━━━━\n👉 <a href="https://in.bookmyshow.com/explore/movies-trichy">Open BMS</a>'
    final_msg = header + meta + body + footer

    # Telegram POST
    try:
        print("Sending message to Telegram...")
        res = requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
            data={
                "chat_id": CHAT_ID, 
                "text": final_msg, 
                "parse_mode": "HTML", # Changed to HTML
                "disable_web_page_preview": "true"
            }
        )
        print(f"Telegram response: {res.status_code}")
        if res.status_code != 200:
            print(f"Telegram Error Details: {res.text}")
    except Exception as e:
        print(f"Telegram Post Error: {e}")

if __name__ == "__main__":
    run_all()
