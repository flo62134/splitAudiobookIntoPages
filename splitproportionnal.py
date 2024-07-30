import os
import subprocess


def get_audio_duration(file_path):
    # Step 0: Get the duration of an audio file
    cmd = [
        'ffprobe',
        '-v', 'error',
        '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1',
        file_path
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE)
    return float(result.stdout)


def split():
    # Step 1: Read the Chapter-Page Mapping File
    chapters_pages_file = './chapters_pages'
    chapters = []
    with open(chapters_pages_file, 'r') as file:
        lines = file.readlines()
        for line in lines:
            # Split from the right only once if the file name contains commas
            audio_file, start_page = line.rsplit(',', 1)
            chapters.append((audio_file.strip(), int(start_page.strip())))

    # Step 2: Read the Last Page Number
    with open('./audiobook_end_page', 'r') as file:
        audiobook_end_page = int(file.readline().strip())

    # Step 3: Calculate Pages for Each Chapter
    for i, chapter in enumerate(chapters):
        start_page = chapter[1]
        end_page = chapters[i + 1][1] - 1 if i + 1 < len(chapters) else audiobook_end_page

        # Step 4: Split Audio Files
        num_pages = end_page - start_page + 1
        audio_file_path = chapter[0]
        chapter_duration = get_audio_duration(audio_file_path)
        page_duration = chapter_duration / num_pages
        output_path = './audiobook_pages/{}-temp.mp3'

        # Use ffmpeg to split the audio file into equal parts with the best possible quality
        cmd = [
            'ffmpeg',
            '-i', audio_file_path,
            '-map_metadata', '-1',
            '-f', 'segment',
            '-segment_time', str(page_duration),
            '-c:a', 'libmp3lame',  # Specify the audio codec
            '-q:a', '0',  # Set the quality to best (VBR)
            output_path.format('%d')  # Ensure output files are properly numbered
        ]
        subprocess.run(cmd)

        # Step 5: Rename the Split Audio Files to Page Numbers
        for j in range(num_pages):
            old_file_path = output_path.format(j)
            new_file_name = str(start_page + j) + '.mp3'
            new_file_path = os.path.join('./audiobook_pages', new_file_name)
            os.rename(old_file_path, new_file_path)


if __name__ == '__main__':
    split()
