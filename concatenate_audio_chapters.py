import os
import subprocess


def concatenate():
    # Get the list of all files in the directory
    directory_path = './audiobook_chapters'
    file_names = sorted(os.listdir(directory_path))

    # Create a text file containing the names of all audio files to concatenate
    with open('concat_list.txt', 'w') as f:
        for file_name in file_names:
            if file_name.endswith('.mp3'):
                f.write(f"file '{os.path.join(directory_path, file_name)}'\n")

    # Run ffmpeg command to concatenate the audio files
    output_file = 'concatenated_audio.mp3'
    subprocess.run(['ffmpeg', '-f', 'concat', '-safe', '0', '-i', 'concat_list.txt', '-c:a', 'libmp3lame', '-q:a', '0',
                    output_file])

    # Remove the temporary text file
    os.remove('concat_list.txt')


if __name__ == '__main__':
    concatenate()
