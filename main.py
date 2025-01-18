from os import scandir, rename
from os.path import splitext, exists, join
from shutil import move
import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

#image file types
image_e = (".jpg", ".jpeg", ".jpe", ".jif", ".jfif", ".jfi", ".png", ".gif", ".webp", ".tiff", ".tif", ".psd", ".raw", ".arw", ".cr2", ".nrw",
                    ".k25", ".bmp", ".dib", ".heif", ".heic", ".ind", ".indd", ".indt", ".jp2", ".j2k", ".jpf", ".jpf", ".jpx", ".jpm", ".mj2", ".svg", ".svgz", ".ai", ".eps", ".ico")
#video file types
video_e = (".webm", ".mpg", ".mp2", ".mpeg", ".mpe", ".mpv", ".ogg",
                    ".mp4", ".mp4v", ".m4v", ".avi", ".wmv", ".mov", ".qt", ".flv", ".swf", ".avchd")
#audio file types
audio_e = (".m4a", ".flac", "mp3", ".wav", ".wma", ".aac")
#document file types
docs_e = (".doc", ".docx", ".odt",
                       ".pdf", ".xls", ".xlsx", ".ppt", ".pptx")

dest_audio = "/Users/sallydavies/Downloads/dl_audio"
dest_video = "/Users/sallydavies/Downloads/dl_video"
dest_docs = "/Users/sallydavies/Downloads/dl_docs"
dest_images = "/Users/sallydavies/Downloads/dl_images"
dest_misc = "/Users/sallydavies/Downloads/dl_misc"
 
dl_dir = "/Users/sallydavies/Downloads"

#if the file already exists in the folder, create a unique name
def unique_name(destination, file_name):
    filename, extension = splitext(file_name)
    count = 1
    while exists(f"{destination}/{file_name}"):
        file_name = f"{filename}({str(count)}){extension}"
        count += 1 
    return file_name

#function that moves the files 
def move(destination, dl_file, file_name):
    if exists(f"{destination}/{file_name}"):
        u_name = unique_name(destination, file_name)
        old_name = join(destination, file_name)
        new_name = join(destination, u_name)
        rename(old_name,new_name)
    move(dl_file, destination)


#create a file handler class that inherits from the watchdog module class
class FileHandler(LoggingEventHandler):

    def on_modified(self, event):
        #run a for loop to access all the files in the downloads file
        with scandir(dl_dir) as dl_files:
            for dl_file in dl_files:
                file_name = dl_file.name
                self.check_audio(dl_file, file_name)
                self.check_video(dl_file, file_name)
                self.check_docs(dl_file, file_name)
                self.check_images(dl_file, file_name)
                self.check_misc(dl_file, file_name)

    def check_audio(self, dl_file, file_name):
        #check for audio files, if is an audio file, move to the audio folder
        for a_e in audio_e:
            if file_name.endswith(audio_e) or file_name.endswith(audio_e.upper()):
                destination = dest_audio
            move(destination, dl_file, file_name)
            logging.info(f"{file_name} successfully moved to audio folder")

    def check_video(self, dl_file, file_name):
        #check for video files, if is an video file, move to the video folder
        for v_e in video_e:
            if file_name.endswith(video_e) or file_name.endswith(video_e.upper()):
                destination = dest_video
            move(destination, dl_file, file_name)
            logging.info(f"{file_name} successfully moved to video folder")

    def check_docs(self, dl_file, file_name):
        #check for doc files, if is an doc file, move to the doc folder
        for d_e in docs_e:
            if file_name.endswith(docs_e) or file_name.endswith(docs_e.upper()):
                destination = dest_docs
            move(destination, dl_file, file_name)
            logging.info(f"{file_name} successfully moved to docs folder")

    def check_images(self, dl_file, file_name):
        #check for image files, if is an image file, move to the image folder
        for i_e in image_e:
            if file_name.endswith(image_e) or file_name.endswith(image_e.upper()):
                destination = dest_images
            move(destination, dl_file, file_name)
            logging.info(f"{file_name} successfully moved to images folder")



#initiate the watchdog module
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = dl_dir
    event_handler = FileHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()