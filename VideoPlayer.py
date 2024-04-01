import cv2
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import math
class VideoPlayerFrame(tk.Frame):
    def __init__(self, master=None, video_path=None):
        super().__init__(master)
        self.master = master
        self.video_path = video_path
        self.paused = False

        # Create a label to display the video
        self.label = tk.Label(self)
        self.label.pack(fill="both", expand=True)

        # Load the video and play it
        self.video = cv2.VideoCapture(video_path)
        self.video_width = int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.video_height = int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.play_video()


    def play_video(self):
        if not self.paused:
            ret, frame = self.video.read()
            if ret:
                # Resize the frame to fit the label
                maxVidWidth=self.master.winfo_screenwidth()
                maxVidHeight = 745
                
                imgWidth = min(round((self.video_width / self.video_height) * maxVidHeight), maxVidWidth)
                imgHeight = min(maxVidHeight, round((self.video_height / self.video_width) * maxVidWidth))
                frame = cv2.resize(frame, (imgWidth, imgHeight))

                # Convert the frame to RGB format
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Convert the frame to a Tkinter-compatible image
                img = Image.fromarray(frame)
                img = ImageTk.PhotoImage(image=img)

                # Update the label with the new frame
                self.label.config(image=img)
                self.label.img = img

                # Continue playing the video
                self.master.after(10, self.play_video)
            else:
                # Reset the video when it reaches the end
                self.reset_video()


    def toggle_pause_resume(self):
        if self.paused:
            # Resume playing the video
            self.paused = False

            self.play_video()
        else:
            # Pause the video
            self.paused = True

    def reset_video(self):
        # Set video position to the start
        self.video.set(cv2.CAP_PROP_POS_FRAMES, 0)
        # Pause the video
        self.paused = True


    def get_video_duration(self):
        # Open the video source
        video = cv2.VideoCapture(self.video_path)

        # Get the total number of frames
        total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

        # Get the frame rate
        fps = int(video.get(cv2.CAP_PROP_FPS))

        # Calculate the duration in seconds
        duration_sec = total_frames / fps

        # Close the video source
        video.release()

        return math.floor(duration_sec)

