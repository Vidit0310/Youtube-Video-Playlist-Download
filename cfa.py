import subprocess
import os


def get_video_formats(url):
    """Show all formats available for a video."""

    command = [
        'yt-dlp',
        '--js-runtimes', 'node',
        '--cookies-from-browser', 'firefox',
        '-F',
        url
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    print(result.stdout)

    if result.stderr:
        print(result.stderr)


def download_video(url, output_folder):
    """Download a single video in the maximum available quality."""

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    output_path = os.path.join(
        output_folder,
        '%(title)s.%(ext)s'
    )

    command = [
        'yt-dlp',

        # Use Node.js for YouTube JS challenges
        '--js-runtimes', 'node',

        # Use the logged-in Firefox YouTube account
        '--cookies-from-browser', 'firefox',

        # Best available video + best available audio
        '-f', 'bv*+ba/b',

        # Output filename
        '-o', output_path,

        # Don't overwrite an existing file
        '--no-overwrites',

        url
    ]

    subprocess.run(command)


def download_playlist(
    playlist_url,
    output_folder,
    start_index=1
):
    """Download playlist videos in maximum available quality."""

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    output_path = os.path.join(
        output_folder,
        '%(playlist_index)03d - %(title)s.%(ext)s'
    )

    command = [
        'yt-dlp',

        # Use Node.js to solve YouTube JS challenges
        '--js-runtimes', 'node',

        # Use Firefox's logged-in YouTube account
        '--cookies-from-browser', 'firefox',

        # Best available video + best available audio
        '-f', 'bv*+ba/b',

        # Output filename
        '-o', output_path,

        # Start from specified playlist index
        '--playlist-start', str(start_index),

        # Keep already downloaded files
        '--no-overwrites',

        # Remember successfully downloaded videos
        '--download-archive', 'downloaded.txt',

        playlist_url
    ]

    subprocess.run(command)


# ============================================================
# MAIN
# ============================================================

playlist_url = (
    'https://www.youtube.com/playlist?list=PLEXCZVdgvUlCeYQbUwU6TO0kULldTnlfe'
)

output_folder = 'videos'

# Start from video 1
start_index = 1


download_playlist(
    playlist_url,
    output_folder,
    start_index
)