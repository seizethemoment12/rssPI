import tkinter as tk
from PIL import Image, ImageTk
import requests
from io import BytesIO
import feedparser
import threading
import time

# URL of the RSS feed
#RSS_FEED_URL = 'https://darkreading.com/rss.xml'
RSS_FEED_URL = 'https://www.bleepingcomputer.com/feed/'

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
    while True:  # Outer loop to fetch the RSS feed every hour
        entries = fetch_rss()  # Fetch the latest entries
        start_time = time.time()  # Record the start time
        
        # Inner loop to cycle through the articles
        while time.time() - start_time < 3600:  # Continue cycling for one hour
            for entry in entries:
                if 'media_content' in entry:
                    image_url = entry.media_content[0]['url']
                    response = requests.get(image_url)
                    img_data = Image.open(BytesIO(response.content))
                    resized_img_data = resize_image(img_data, label_image.winfo_width(), label_image.winfo_height())
                    img = ImageTk.PhotoImage(resized_img_data)

                    label_image.config(image=img)
                    label_image.image = img  # Keep a reference to avoid garbage collection

                label_title.config(text=entry.title)
                label_summary.config(text=entry.summary)
                root.update_idletasks()  # Update the GUI
                
                time.sleep(20)  # Wait for 20 seconds before showing the next article

                # Check if an hour has passed
                if time.time() - start_time >= 3600:
                    break

# Methods for handling fullscreen
def toggle_fullscreen(event=None):
    root.attributes('-fullscreen', not root.attributes('-fullscreen'))
    return "break"
    
def end_fullscreen(event=None):
    root.attributes('-fullscreen', False)
    return "break"
    

# Set up the tkinter GUI
root = tk.Tk()
root.title("OSINT")

# Setup the keybindings
root.bind('<F11>', toggle_fullscreen)
root.bind('<Escape>', end_fullscreen)

# Start in full screen
root.attributes('-fullscreen', True)

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
root.grid_rowconfigure(0, weight=1) # Image
root.grid_rowconfigure(1, weight=3) # Title
root.grid_rowconfigure(2, weight=1)# Summary


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
