import os
import csv
import re
from bs4 import BeautifulSoup


def read_chapters_map(file_path):
    """
    Read the chapters_map file and create a mapping between audiobook files and epub files.

    Args:
    file_path (str): Path to the chapters_map file.

    Returns:
    dict: A dictionary where the key is the audiobook filename and the value is the ebook filename.
    """
    mapping = {}
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            audiobook_filename, ebook_filename = row
            mapping[audiobook_filename.strip()] = ebook_filename.strip()

    return mapping


def create_directories():
    """
    Create the necessary directories if they don't already exist.
    """
    os.makedirs('./alignment', exist_ok=True)
    os.makedirs('./audiobook_pages', exist_ok=True)


def run_echogarden_align(audiobook_to_ebook_map):
    """
    Run the echogarden align command for every pair of audiobook and ebook files.

    Args:
    audiobook_to_ebook_map (dict): A mapping between audiobook files and epub files.
    """
    for audiobook_filename, ebook_filename in audiobook_to_ebook_map.items():
        alignment_srt_filename = f'./alignment/{audiobook_filename}-{ebook_filename}.srt'
        alignment_json_filename = f'./alignment/{audiobook_filename}-{ebook_filename}.json'

        # Here is where you should run the echogarden align command.
        # Replace the following comment with the actual command.
        #
        os.system(
            f'echogarden align "./audiobook_chapters/{audiobook_filename}" "./ebook_files/text/{ebook_filename}" "{alignment_srt_filename}" "{alignment_json_filename}"')
        #
        print(f"Align command would be run for {audiobook_filename} and {ebook_filename}")


def read_audiobook_pages(file_path):
    """
    Read the audiobook_pages file and parse the start and end page numbers.

    Args:
    file_path (str): Path to the audiobook_pages file.

    Returns:
    list: A list of tuples where each tuple contains the start and end page numbers.
    """
    pages = []
    with open(file_path, 'r') as file:
        for line in file:
            start_page, end_page = map(int, line.strip().split(','))
            pages.append((start_page, end_page))
    return pages


def extract_text_from_html(ebook_filename, page_number):
    """
    Parse the HTML file to find the <span> tag with the specified ID and attributes,
    and then locate the preceding <p> tag to extract its text content.

    Args:
    ebook_filename (str): The filename of the ebook HTML file.
    page_number (int): The page number to search for in the HTML file.

    Returns:
    str: The text content of the preceding <p> tag, or None if not found.
    """
    with open(f'./ebook_files/text/{ebook_filename}', 'r') as file:
        soup = BeautifulSoup(file, 'html.parser')
        span_tag = soup.find('span', {'id': f'pg{page_number + 1}', 'epub:type': 'pagebreak'})

        if span_tag:
            p_tag = span_tag.find_previous('p').find_previous('p')
            if p_tag:
                return p_tag.get_text()

    return None


def split_audio_file(audiobook_filename, start_time, end_time, output_filename):
    """
    Use ffmpeg to split the audio file based on the timestamps.

    Args:
    audiobook_filename (str): The filename of the audiobook file.
    start_time (str): The start timestamp to split the audio file.
    end_time (str): The end timestamp to split the audio file.
    output_filename (str): The filename for the output audio file.
    """
    # Here is where you should run the ffmpeg command.
    # Replace the following comment with the actual command.
    #
    start_time = start_time.replace(',', '.')
    end_time = end_time.replace(',', '.')
    os.system(f'ffmpeg -i "./audiobook_chapters/{audiobook_filename}" -ss {start_time} -to {end_time} -c copy "./audiobook_pages/{output_filename}"')

    #
    print(
        f"FFMPEG command would be run for {audiobook_filename} from {start_time} to {end_time} with output file {output_filename}")


def get_end_timestamp_from_srt(srt_file_path, search_text):
    """
    Read a .srt file, search for a given text content, and retrieve the end timestamp of that content.

    Args:
    srt_file_path (str): Path to the .srt file.
    search_text (str): The text content to search for in the .srt file.

    Returns:
    str: The end timestamp of the content if found, or None otherwise.
    """
    # Regular expression pattern for time range in SRT file
    time_range_pattern = re.compile(r'(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})')

    with open(srt_file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        # If the current line contains the search_text
        if search_text in line:
            # Look for the time range in the previous lines
            for j in range(i, -1, -1):
                match = time_range_pattern.search(lines[j])
                if match:
                    # Return the end timestamp
                    return match.group(2)

    return None


if __name__ == '__main__':
    # Define the paths for input and output directories/files
    chapters_map_file_path = './chapters_map'
    audiobook_pages_file_path = './audiobook_start_end_pages'
    ebook_files_path = './ebook_files/text/'
    audiobook_chapters_path = './audiobook_chapters/'
    alignment_path = './alignment/'
    audiobook_pages_path = './audiobook_pages/'

    # Step 1: Read the Chapters Map
    audiobook_to_ebook_map = read_chapters_map(chapters_map_file_path)

    # Step 2: Create Directories
    create_directories()

    # Step 3: Run Echogarden Align
    # run_echogarden_align(audiobook_to_ebook_map)

    # Step 4: Read Audiobook Pages
    audiobook_pages = read_audiobook_pages(audiobook_pages_file_path)

    # Step 5: Extract Text and Split Audio
    for start_page, end_page in audiobook_pages:
        for page_number in range(start_page, end_page + 1):
            for audiobook_filename, ebook_filename in audiobook_to_ebook_map.items():

                # Extract text content from the HTML file
                text_content = extract_text_from_html(ebook_filename, page_number)

                if text_content:
                    # Construct the path to the corresponding .srt file
                    srt_file_path = os.path.join(alignment_path, f'{audiobook_filename}-{ebook_filename}.srt')

                    # Search for this text content in the .srt file
                    end_timestamp = get_end_timestamp_from_srt(srt_file_path, text_content)

                    if end_timestamp:
                        # Construct the path to the output audio file
                        output_audio_filename = f'{page_number}.mp3'
                        output_audio_filepath = os.path.join(audiobook_pages_path, output_audio_filename)

                        # Use ffmpeg to split the audio file based on the timestamps
                        split_audio_file(audiobook_filename, '0', end_timestamp, output_audio_filename)
