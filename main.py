
# Press the green button in the gutter to run the script.
if __name__ == '__main__':


# This script splits an audiobook into pages, based on the pages found in an epub file.
# Epub file will be located in ./ebook_files
# The epub file will have been extracted by the user
# The epub text files will be located in ./ebook_files/text

# Audiobook will be located in ./audiobook_chapters
# ./audiobook_chapters contains multiple files, each representing a chapter of the audiobook
# Files in ./audiobook_chapters can be sorted numerically in order to sort them by chapter

# File ./chapters_map contains a list of audiobook files related to epub files
# An audiobook file can be mapped to only one epub file
# ./chapters_map contains lines that follow this format:
# AUDIOFILENAME, EBOOKFILENAME
# Example: Project Hail Mary [B08GB66Q3R] - 03 - Chapter 1.mp3, part0007.html

# Create directory ./alignment
# This directory will contain alignment files between audiobook files and ebook files
# For every couple of files, run the following command on the local computer:
# echogarden align ./audiobook_chapters/AUDIOBOOKFILENAME  ./ebook_files/text/EBOOKFILENAME ./alignment/AUDIOBOOKFILENAME-EBOOKFILENAME.srt ./alignment/AUDIOBOOKFILENAME-EBOOKFILENAME.json

# Create directory ./audiobook_pages
# File pages contain two pages numbers, separated by a comma.
# Example: 3, 479

# Iterate over start page and end page.
# For every page in ./audiobook_pages
    # Search for html tag <span> with id equal to "pg{PAGENUMBER+1}" and attribute epub:type="pagebreak"
    # If the first page is 3, you will look for: <span id="pg4" epub:type="pagebreak" class="calibre">
    # Look for the previous HTML <p> tag and retrieve its text content.
    # Look for this text content in ./alignment/AUDIOBOOKFILENAME-EBOOKFILENAME.srt
    # Retrieve the end timestamp of this text content
    # Using FFMPEG, split ./audiobook_chapters/AUDIOBOOKFILENAME from the beginning of the previous chapter (or start at 0 if it does not exist) to the end timestamp of the content
    # The audio file result must be put in ./audiobook_pages/PAGENUMBER
    # For example: the first audio file will be ./audiobook_pages/3
