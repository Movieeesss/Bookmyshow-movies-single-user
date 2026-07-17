import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, timezone

# --- CONFIGURATION (Keep your keys safe!) ---
TOKEN = "8745585993:AAE2zRpimM9_VW9YK0I7FhDmvHb7iy1tw9A"
CHAT_ID = "1115358053"
API_KEY = "45b4f3e2-b8db-473c-8b38-374fa0b0febe"

def get_trichy_movies():
    target_url = "https://in.bookmyshow.com/explore/movies-trichy"
    # Render=true and wait=10000 is good for JS heavy sites like BMS
    proxy_url = f"https://api.webscraping.ai/html?api_key={API_KEY}&url={target_url}&proxy=residential&render=true&wait=10000"
    
    movie_list = set() 
    try:
        # Timeout 45s kudukrom because render=true takes time
        response = requests.get(proxy_url, timeout=45)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Method 1: H3 tags check
            for h3 in soup.find_all('h3'):
                name = h3.get_text().strip().upper()
                
                # Filtering logic
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
        else:
            print(f"Scraper Error: Status {response.status_code}")
            
    except Exception as e:
        print(f"Connection Error: {e}")
        
    return sorted(list(movie_list))

def run_all():
    movies = get_trichy_movies()
    
    ist_now = datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)
    time_str = ist_now.strftime("%d-%m-%Y | %I:%M %p")
    
    header = "🎬 *TRICHY MOVIES LIST* 🎬\n"
    meta = f"🕒 {time_str}\n━━━━━━━━━━━━━━━━━━━━\n"
    
    if not movies:
        body = "⚠️ *Status:* No movies detected. Check Proxy/API Key.\n"
    else:
        body = "🎥 *NOW SHOWING:*\n\n"
        for m in movies:
            body += f"✅ *{m}*\n"
            
    footer = "\n━━━━━━━━━━━━━━━━━━━━\n👉 [Open BMS](https://in.bookmyshow.com/explore/movies-trichy)"
    final_msg = header + meta + body + footer

    # Telegram POST
    try:
        res = requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
            data={
                "chat_id": CHAT_ID, 
                "text": final_msg, 
                "parse_mode": "Markdown", 
                "disable_web_page_preview": "true"
            }
        )
        print(f"Telegram response: {res.status_code}")
    except Exception as e:
        print(f"Telegram Error: {e}")

if __name__ == "__main__":
    run_all()
