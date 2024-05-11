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

# Resize the image
def resize_image(img_data, target_width, target_height):
    original_width, original_height = img_data.size
    ratio = min(target_width / original_width, target_height / original_height)
    new_width = int(original_width * ratio)
    new_height = int(original_height * ratio)
    return img_data.resize((new_width, new_height), Image.Resampling.LANCZOS)

# Update the news article display every 20 seconds
def update_news():
    for entry in fetch_rss():
        if 'media_content' in entry:
            image_url = entry.media_content[0]['url']
            response = requests.get(image_url)
            img_data = Image.open(BytesIO(response.content))
            resized_img_data = resize_image(img_data, label_image.winfo_width(), label_image.winfo_height())
            # Resize the image to fit
            
            img = ImageTk.PhotoImage(resized_img_data)
            label_image.config(image=img)
            label_image.image = img  # keep a reference!

        label_title.config(text=entry.title)
        label_summary.config(text=entry.summary)
        root.update()
        time.sleep(20)  # delay before showing the next article

# Set up the tkinter GUI
root = tk.Tk()
root.title("OSINT")

# Center and appropriately size the window
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_width = int(screen_width * 0.95)
window_height = int(screen_height * 0.95)
x_offset = int((screen_width - window_width) / 2)
y_offset = int((screen_height - window_height) / 2)
root.geometry(f'{window_width}x{window_height}+{x_offset}+{y_offset}')

#Use a grid to make the labels scale
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=3)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)


label_image = tk.Label(root)
label_image.grid(row=0, column=0, sticky='nsew')

label_title = tk.Label(root, font=('Arial', 20), wraplength=500)
label_title.grid(row=1, column=0, sticky='nsew')

label_summary = tk.Label(root, font=('Arial', 14), wraplength=500)
label_summary.grid(row=2, column=0, sticky='nsew')

# Start the update thread
thread = threading.Thread(target=update_news)
thread.daemon = True
thread.start()

root.mainloop()
