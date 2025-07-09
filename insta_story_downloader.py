import os
import sys
import threading
from tkinter import *
from tkinter import messagebox
import instaloader
from datetime import datetime

# Output path setup
if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(os.path.abspath(__file__))

output_dir = os.path.join(os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else base_path, "stories")
os.makedirs(output_dir, exist_ok=True)

# GUI Function
def download_stories():
    username = username_entry.get().strip()
    if not username:
        messagebox.showerror("Error", "Enter a valid Instagram username")
        return

    status_label.config(text="🔄 Downloading...", fg="blue")
    download_button.config(state=DISABLED)

    def run():
        try:
            L = instaloader.Instaloader(dirname_pattern=os.path.join(output_dir, username, "{date_utc}"))

            # Login as anonymous (public only)
            profile = instaloader.Profile.from_username(L.context, username)
            stories = L.get_stories(userids=[profile.userid])

            found = False
            for story in stories:
                for item in story.get_items():
                    found = True
                    L.download_storyitem(item, os.path.join(output_dir, username))
            if found:
                status_label.config(text=f"✅ Stories saved in /stories/{username}", fg="green")
            else:
                status_label.config(text="ℹ️ No public stories available", fg="orange")
        except Exception as e:
            status_label.config(text=f"❌ Error: {str(e)}", fg="red")
        finally:
            download_button.config(state=NORMAL)

    threading.Thread(target=run).start()

# GUI Setup
root = Tk()
root.title("Instagram Story Downloader")
root.geometry("400x250")
root.resizable(False, False)

Label(root, text="📸 Instagram Story Downloader", font=("Segoe UI", 14, "bold")).pack(pady=10)

Label(root, text="Instagram Username:", font=("Segoe UI", 10)).pack(pady=(20, 5))
username_entry = Entry(root, width=40)
username_entry.pack()

download_button = Button(root, text="⬇️ Download Stories", command=download_stories, bg="green", fg="white", font=("Segoe UI", 10, "bold"))
download_button.pack(pady=20)

status_label = Label(root, text="", font=("Segoe UI", 10))
status_label.pack()

Label(root, text="by d0wnbad.hu", font=("Courier New", 10, "italic"), fg="gray").pack(side="bottom", pady=10)

root.mainloop()
