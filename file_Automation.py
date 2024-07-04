import sys
import time
import logging
from os import scandir, rename
from shutil import move
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler, FileSystemEventHandler
from os.path import splitext, exists, join

source_dir = r"C:\Users\gnoul\OneDrive\Downloads" #location where downloads normally go

#specific locations I want to organize them to
destination_directory_sfx = r"C:\Users\gnoul\OneDrive\Downloaded Sounds"
destination_directory_music = r"C:\Users\gnoul\OneDrive\Downloaded Music"
destination_directory_video = r"C:\Users\gnoul\OneDrive\Downloaded Videos"
destination_directory_image = r"C:\Users\gnoul\OneDrive\Downloaded Images"
destination_directory_document = r"C:\Users\gnoul\OneDrive\Downloaded Documents"

# ? supported image types
image_extensions = (".jpg", ".jpeg", ".jpe", ".jif", ".jfif", ".jfi", ".png", ".gif", ".webp", ".tiff", ".tif", ".psd", ".raw", ".arw", ".cr2", ".nrw",
                    ".k25", ".bmp", ".dib", ".heif", ".heic", ".ind", ".indd", ".indt", ".jp2", ".j2k", ".jpf", ".jpf", ".jpx", ".jpm", ".mj2", ".svg", ".svgz", ".ai", ".eps", ".ico")
# ? supported Video types
video_extensions = (".webm", ".mpg", ".mp2", ".mpeg", ".mpe", ".mpv", ".ogg",
                    ".mp4", ".mp4v", ".m4v", ".avi", ".wmv", ".mov", ".qt", ".flv", ".swf", ".avchd")
# ? supported Audio types
audio_extensions = (".m4a", ".flac", "mp3", ".wav", ".wma", ".aac")
# ? supported Document types
document_extensions = (".doc", ".docx", ".odt",
                       ".pdf", ".xls", ".xlsx", ".ppt", ".pptx")


# function to make a name to allow the categroization function
def makeUnique(destination, name):
    filename, extension = splitext(name)
    counter = 1
# if file already exist add a number to the name
    while exists(f"{destination}/{name}"):
        name = f"{filename}({str(counter)}){extension}"
        counter+=1
    return name

def move_files(destination, entry, name):
    if exists(f"{destination}/{name}"):
        uniqueName = makeUnique(destination,name)
        oldName = join(destination,name)
        newName = join(destination, uniqueName)
        rename(oldName,newName)
    move(entry, destination)


class OrganizingHandler(FileSystemEventHandler):
    def on_modified(self, event):
        with scandir(source_dir) as entries: # scanning function for the folders on device
            for entry in entries: #loop through all the entries that are in the downloads folder
                name = entry.name
                destination = source_dir
                if name.endswith(audio_extensions): # list of if conditions to categorize where the downloaded file will end up
                    if entry.stat().st_size < 25000000 or "SFX" in name:
                        destination = destination_directory_sfx
                    else:
                        destination =  destination_directory_music
                    move_files(destination, entry, name)
                    logging.info(f"Moved audio file: {name}")
                elif name.endswith(video_extensions):
                    destination = destination_directory_video
                    move_files(destination, entry, name)
                    logging.info(f"Moved video file: {name}")
                elif name.endswith(image_extensions):
                    destination = destination_directory_image
                    move_files(destination, entry, name)
                    logging.info(f"Moved image file: {name}")
                elif name.endswith(document_extensions):
                    destination = destination_directory_document
                    move_files(destination, entry, name)
                    logging.info(f"Moved document file: {name}")

if __name__ == "__main__": # imported logic to react to a change in the download folder.
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = source_dir
    event_handler = OrganizingHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()