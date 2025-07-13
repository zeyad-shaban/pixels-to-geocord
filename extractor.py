import numpy as np
from pathlib import Path
from PIL import Image
from gopro_overlay.ffmpeg import FFMPEG
from gopro_overlay.ffmpeg_gopro import FFMPEGGoPro
from gopro_overlay.timeunits import timeunits
import matplotlib.pyplot as plt


video_path = "./data/GX011072.MP4"
frame_number = 3675
fps = 30

ffmpeg_gopro = FFMPEGGoPro(FFMPEG())
recording = ffmpeg_gopro.find_recording(video_path)

dimensions = recording.video.dimension
# Extract frame at specific time (e.g., 2 seconds)
frame_time = timeunits(seconds=frame_number / fps)
frame_data = ffmpeg_gopro.load_frame(Path(video_path), frame_time)

if frame_data:
    # Convert raw RGBA bytes to PIL Image
    frame_image = Image.frombytes(mode="RGBA", size=dimensions.tuple(), data=frame_data)

    # Display with matplotlib
    fig, ax = plt.subplots(figsize=(12, 8))
    plt.imshow(frame_image)
    plt.axis("off")  # Hide axes
    plt.title(f"Video Frame at {frame_time}")
    
    # Initialize variables for frame navigation
    current_frame = frame_number
    total_frames = recording.video.frame_count
    
    # Initialize dot object
    dot = None
    
    def onclick(event):
        global dot
        if event.xdata is not None and event.ydata is not None:
            # Remove previous dot if it exists
            if dot is not None:
                dot.remove()
            
            # Add new dot at clicked position
            dot = ax.plot(event.xdata, event.ydata, 'ro')[0]
            print(f"Clicked at: ({event.xdata:.2f}, {event.ydata:.2f})")
            fig.canvas.draw()
    
    def on_key(event):
        global current_frame, dot
        
        if event.key == 'right':
            # Move to next frame
            if current_frame < total_frames - 1:
                current_frame += 1
            else:
                print("Already at last frame")
                return
        elif event.key == 'left':
            # Move to previous frame
            if current_frame > 0:
                current_frame -= 1
            else:
                print("Already at first frame")
                return
        
        try:
            # Update frame
            frame_time = timeunits(seconds=current_frame / fps)
            frame_data = ffmpeg_gopro.load_frame(Path(video_path), frame_time)
            
            if frame_data:
                # Convert frame data to image
                frame_image = Image.frombytes(mode="RGBA", size=dimensions.tuple(), data=frame_data)
                
                # Clear existing image and plot new frame
                ax.clear()
                ax.imshow(frame_image)
                ax.axis("off")
                ax.set_title(f"Video Frame at {frame_time}")
                
                # Redraw dot if it exists
                if dot is not None:
                    dot.remove()
                    dot = ax.plot(dot.get_xdata()[0], dot.get_ydata()[0], 'ro')[0]
                
                fig.canvas.draw()
            else:
                print(f"Failed to load frame {current_frame}")
        except Exception as e:
            print(f"Error updating frame: {str(e)}")
    
    # Connect events
    cid_click = fig.canvas.mpl_connect('button_press_event', onclick)
    cid_key = fig.canvas.mpl_connect('key_press_event', on_key)
    
    plt.show()