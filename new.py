# import os
# import yt_dlp

# def download_video(video_url, output_dir="videos"):
#     os.makedirs(output_dir, exist_ok=True)
#     ydl_opts = {
#         'outtmpl': f'{output_dir}/%(title)s.%(ext)s',
#         'format': 'best',
#     }
#     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#         ydl.download([video_url])

# def download_playlist(playlist_url, output_dir="videos"):
#     os.makedirs(output_dir, exist_ok=True)
#     ydl_opts = {
#         'outtmpl': f'{output_dir}/%(playlist_index)s - %(title)s.%(ext)s',
#         'format': 'best',
#         'yes_playlist': True,
#     }
#     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#         ydl.download([playlist_url])

# # Main
# playlist_url = input("Enter playlist or video link:\n")
# if 'playlist' in playlist_url:
#     download_playlist(playlist_url)
# else:
#     download_video(playlist_url)



import os
import subprocess

def get_video_formats(url):
    """List available formats for the given video URL."""
    command = ['yt-dlp', '-F', url]
    result = subprocess.run(command, capture_output=True, text=True)
    print(result.stdout)  # Print available formats for inspection

def download_video_and_audio(url, output_folder):
    """Download video and audio streams separately and merge them using ffmpeg."""
    os.makedirs(output_folder, exist_ok=True)

    # Paths for the separate streams
    video_path = os.path.join(output_folder, 'video.mp4')
    audio_path = os.path.join(output_folder, 'audio.m4a')
    output_path = os.path.join(output_folder, '%(title)s.mp4')

    # Download video (format 136 for 720p video)
    command_video = ['yt-dlp', '-f', '136', '-o', video_path, url]
    subprocess.run(command_video)

    # Download audio (format 140 for audio)
    command_audio = ['yt-dlp', '-f', '140', '-o', audio_path, url]
    subprocess.run(command_audio)

    # Merge video and audio using ffmpeg
    merged_output_path = os.path.join(output_folder, 'output.mp4')
    merge_command = [
        'ffmpeg', '-i', video_path, '-i', audio_path, '-c:v', 'copy', '-c:a', 'aac', merged_output_path
    ]
    subprocess.run(merge_command)

    # Cleanup temporary files
    os.remove(video_path)
    os.remove(audio_path)

    print(f"Downloaded and merged video saved to {merged_output_path}")

def download_playlist(playlist_url, output_folder):
    """Download all public videos in a playlist."""
    os.makedirs(output_folder, exist_ok=True)

    # Get list of video URLs in the playlist
    command_list = ['yt-dlp', '--flat-playlist', '-J', playlist_url]
    result = subprocess.run(command_list, capture_output=True, text=True)
    playlist_data = result.stdout

    if not playlist_data:
        print("Failed to fetch playlist information.")
        return

    # Extract URLs from the playlist
    import json
    playlist_info = json.loads(playlist_data)
    video_urls = [f"https://www.youtube.com/watch?v={entry['id']}" for entry in playlist_info.get('entries', [])]

    # Download each video
    for index, video_url in enumerate(video_urls, start=1):
        print(f"Downloading video {index}/{len(video_urls)}: {video_url}")
        download_video_and_audio(video_url, output_folder)

# Example usage
playlist_url = input("Enter playlist URL: ")  # Public playlist URL
output_folder = "videos"  # Output folder
download_playlist(playlist_url, output_folder)


