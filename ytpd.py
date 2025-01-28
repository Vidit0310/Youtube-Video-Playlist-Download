import os
from pytube import YouTube
import yt_dlp


def sanitize_filename(title):
    # Replace problematic characters with underscores
    return ''.join(c if c.isalnum() or c in [' ', '-'] else '_' for c in title)


def get_playlist_links(playlist_url):
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(playlist_url, download=False)
        if 'entries' in result:
            return [entry['url'] for entry in result['entries']]
        return []


def download_video(link, output_folder, index=None):
    try:
        yt = YouTube(link)
        stream = yt.streams.get_highest_resolution()
        sanitized_title = sanitize_filename(yt.title)
        
        if index is not None:
            filename = f"{index} - {sanitized_title}.mp4"
        else:
            filename = f"{sanitized_title}.mp4"

        output_path = os.path.join(output_folder, filename)
        stream.download(output_path=output_folder, filename=filename)
        print(f"Downloaded: {filename}")
    except Exception as e:
        print(f"Error downloading video: {e}")


def main():
    os.makedirs('videos', exist_ok=True)
    playlist_url = input("Enter playlist or video link:\n")
    
    if 'playlist' in playlist_url:
        video_links = get_playlist_links(playlist_url)
        for i, link in enumerate(video_links, start=1):
            download_video(link, 'videos', i)
    else:
        download_video(playlist_url, 'videos')


if __name__ == "__main__":
    main()
