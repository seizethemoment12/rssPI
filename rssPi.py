import tkinter as tk
from PIL import Image, ImageTk
import requests
from io import BytesIO
import feedparser
import threading
import time

# URL of the RSS feed
RSS_FEED_URL = 'https://darkreading.com/rss.xml'

# Fetch and parse the RSS feed
def fetch_rss():
    feed = feedparser.parse(RSS_FEED_URL)
    return feed.entries

# Update the news article display every 20 seconds
def update_news():
    for entry in fetch_rss():
        if 'media_content' in entry:
            image_url = entry.media_content[0]['url']
            response = requests.get(image_url)
            img_data = Image.open(BytesIO(response.content))
            img = ImageTk.PhotoImage(img_data)
            label_image.config(image=img)
            label_image.image = img  # keep a reference!

        label_title.config(text=entry.title)
        label_summary.config(text=entry.summary)
        root.update()
        time.sleep(20)  # delay before showing the next article

# Set up the tkinter GUI
root = tk.Tk()
root.title("OSINT")
root.geometry('800x600')

label_image = tk.Label(root, width=600, height=400)
label_image.pack()

label_title = tk.Label(root, font=('Arial', 20), wraplength=500)
label_title.pack()

label_summary = tk.Label(root, font=('Arial', 14), wraplength=500)
label_summary.pack()

# Start the update thread
thread = threading.Thread(target=update_news)
thread.daemon = True
thread.start()

root.mainloop()
