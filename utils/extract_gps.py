from pathlib import Path
from PIL import Image
from gopro_overlay.loading import GoproLoader
from gopro_overlay.framemeta_gpmd import LoadFlag
from gopro_overlay.ffmpeg import FFMPEG
from gopro_overlay.ffmpeg_gopro import FFMPEGGoPro
from gopro_overlay.units import units
from gopro_overlay.timeunits import timeunits
import matplotlib.pyplot as plt

def extract_gps(video_path: str, frame_number: int, fps=30):
    ffmpeg_gopro = FFMPEGGoPro(FFMPEG())
    loader = GoproLoader(ffmpeg_gopro=ffmpeg_gopro, units=units, flags={LoadFlag.ACCL, LoadFlag.CORI, LoadFlag.GRAV})  # Include CORI for orientation
    gopro = loader.load(video_path)
    frame_meta = gopro.framemeta

    # Access data at specific frame/timestamp
    entry = frame_meta.get(timeunits(seconds=frame_number / fps))  # or use millis=1
    if entry:
        lat = entry.point.lat
        lon = entry.point.lon
        alt = entry.alt
        if entry.ori:  # Orientation data available
            yaw = entry.ori.yaw
            pitch = entry.ori.pitch
            roll = entry.ori.roll

    gps_data = {"lat": lat, "lon": lon, "alt": alt, "yaw": yaw, "pitch": pitch, "roll": roll}
    return gps_data


def extract_frame(video_path: str, frame_number, fps):
    ffmpeg_gopro = FFMPEGGoPro(FFMPEG())
    recording = ffmpeg_gopro.find_recording(video_path)
    dimensions = recording.video.dimension
    frame_time = timeunits(seconds=frame_number / fps)
    frame_data = ffmpeg_gopro.load_frame(Path(video_path), frame_time)

    if not frame_data:
        return None

    frame_image = Image.frombytes(mode="RGBA", size=dimensions.tuple(), data=frame_data)
    return frame_image


def log_video_info(video_path: str):
    ffmpeg_gopro = FFMPEGGoPro(FFMPEG())
    recording = ffmpeg_gopro.find_recording(video_path)

    fps = recording.video.frame_rate_numerator / recording.video.frame_rate_denominator
    total_frames = recording.video.frame_count
    duration = recording.video.duration

    print(f"FPS: {fps}")
    print(f"Total frames: {total_frames}")
    print(f"Duration: {duration}")


if __name__ == "__main__":
    video_path = "./data/GX011072.MP4"
    frame_number = 2364
    fps = 30

    print(f"🎬 Extracting GPS from: {video_path}")
    gps_data = extract_gps(video_path, frame_number, fps)

    print(gps_data)
    log_video_info(video_path)

    frame_image = extract_frame(video_path, frame_number, fps)
    # Display with matplotlib
    plt.figure(figsize=(12, 8))
    plt.imshow(frame_image)
    plt.axis("off")  # Hide axes
    plt.title(f"Video Frame at {frame_number}")
    plt.show()
