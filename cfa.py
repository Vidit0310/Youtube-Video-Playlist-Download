import subprocess
import os

def get_video_formats(url, cookies_file):
    # Run yt-dlp to get the formats available for the video
    command = ['yt-dlp', '--cookies', cookies_file, '-F', url]
    result = subprocess.run(command, capture_output=True, text=True)
    
    # Print the formats to the console
    return result.stdout

def download_video(url, cookies_file, output_folder):
    # Run yt-dlp to download the video in 720p (video format 136 + audio format 140)
    output_path = os.path.join(output_folder, '%(title)s.%(ext)s')
    command = ['yt-dlp', '--cookies', cookies_file, '-f', '136+140', '-o', output_path, url]
    subprocess.run(command)

def download_playlist(playlist_url, cookies_file, output_folder, start_index=1):
    # Ensure the 'videos' folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Run yt-dlp to download all videos in the playlist starting from the specified index
    output_path = os.path.join(output_folder, '%(title)s.%(ext)s')
    command = ['yt-dlp', '--cookies', cookies_file, '-f', '136+140', '-o', output_path, '--playlist-start', str(start_index), playlist_url]
    subprocess.run(command)

# Example usage+
playlist_url = 'https://youtube.com/playlist?list=PLEXCZVdgvUlCk7Jr7DlcBfPxbQ_crlnA9&si=COsIaAEM2_7uLbwK'  # Replace with your playlist URL
cookies_file = 'cookies.txt'  # Path to your cookies.txt file
output_folder = 'videos'  # Folder where videos will be saved
start_index = 102  # Start downloading from the 5th video

# set PATH=C:\Users\svidi\OneDrive\Desktop\test\yt downloader\ffmpeg\ffmpeg-7.1-essentials_build\ffmpeg-7.1-essentials_build\bin;%PATH%


download_playlist(playlist_url, cookies_file, output_folder, start_index)
