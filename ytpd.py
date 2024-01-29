import youtube_dl
import os
from pytube import YouTube

def get_playlist_links(playlist_url):
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'force_generic_extractor': True,
        'simulate': True,

        # To start download download from a particular number  
        # 'playliststart': 91, 

    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(playlist_url, download=False)
        if 'entries' in result:
            return [f'https://www.youtube.com/watch?v={entry["url"]}' for entry in result['entries']]
        else:
            return []

def sanitize_filename(title):
    # Replace problematic characters with underscores
    return ''.join(c if c.isalnum() or c in [' ', '-'] else '_' for c in title)

def Download_Playlist(link, i):
    youtubeObject = YouTube(link)
    stream = youtubeObject.streams.get_highest_resolution()
    try:
        # Sanitize the title for creating a valid filename
        sanitized_title = sanitize_filename(youtubeObject.title)

        # Set the output path including the folder and filename
        output_path = os.path.join('videos', f'{i} - {sanitized_title}.mp4')

        stream.download("",output_path )
    except Exception as e:
        print(f"An error has occurred in downloading video - {i}: {e}")
    print("Downloaded", i)


def Download_Video(link):
    youtubeObject = YouTube(link)
    stream = youtubeObject.streams.get_highest_resolution()
    try:
        # Sanitize the title for creating a valid filename
        sanitized_title = sanitize_filename(youtubeObject.title)

        # Set the output path including the folder and filename
        output_path = os.path.join('videos', f'{sanitized_title}.mp4')

        stream.download("",output_path )
    except Exception as e:
        print(f"An error has occurred in downloading video : {e}")
    print("Downloaded")

os.makedirs('videos', exist_ok=True)

# Main 
playlist_url = input("Enter playlist or video link:\n")
if 'playlist' in playlist_url:
    video_links = get_playlist_links(playlist_url)
    i = 1
    for link in video_links:
        Download_Playlist(link, i)
        i += 1
else:
    Download_Video(playlist_url)



