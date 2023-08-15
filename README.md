# Audiobook Page Splitter

## Project Description

This project provides a script to split an audiobook into separate audio files based on the pages of an associated
ebook. The user is required to extract an ebook in EPUB format and provide the audiobook files. The script aligns the
audiobook chapters with the ebook files, identifies specific page breaks in the ebook, and creates separate audio files
corresponding to the pages of the ebook.

## Directory Structure

- `./ebook_files/`: Directory where extracted EPUB files are located. The text files of the ebook should be placed
  under `./ebook_files/text/`.
- `./audiobook_chapters/`: Directory containing multiple audio files, each representing a chapter of the audiobook.
- `./chapters_map`: File containing a list of audiobook files related to ebook files in the
  format `AUDIOFILENAME, EBOOKFILENAME`.
- `./alignment/`: Directory that will contain alignment files between audiobook files and ebook files.
- `./audiobook_pages/`: Directory where the resulting audio files will be saved. Each audio file corresponds to a
  specific page or range of pages from the ebook.

## Usage

1. **Prepare Your Files:**
    - Extract your EPUB file and place the text files in the `./ebook_files/text/` directory.
    - Place your audiobook chapter files in the `./audiobook_chapters/` directory.
    - Create a `chapters_map` file to map each audiobook file to its corresponding ebook file.

2. **Run the Script:**
    - Run the Python script `main.py`

3. **Get the Output:**
    - After running the script, you will find the split audio files in the `./audiobook_pages/` directory. Each audio
      file corresponds to specific pages in the ebook.

## Dependencies

- Python 3.x
- BeautifulSoup4: for parsing HTML files
- ffmpeg: for splitting audio files (install separately)
- echogarden: for aligning audiobook and ebook files (install separately)

### Override echogarden

You need to override /usr/local/lib/node_modules/echogarden/dist/utilities/Timeline.js by adding a `continue` here:  
```js
        for (const sentenceEntry of sentenceTimeline) {
            const wordTimeline = sentenceEntry.timeline;
            if (wordTimeline.length == 0) {
                continue;
                throw new Error("Sentence has no word entries");
            }
            sentenceEntry.startTime = wordTimeline[0].startTime;
            sentenceEntry.endT
        }
```

## Example `chapters_map` File

```
Project Hail Mary [B08GB66Q3R] - 03 - Chapter 1.mp3, part0007.html
Project Hail Mary [B08GB66Q3R] - 04 - Chapter 2.mp3, part0008.html
...
```

## Example `audiobook_pages` File

```
3, 479
480, 961
...
```

## Notes

- Ensure that `ffmpeg` and `echogarden` (or a similar alignment tool) are installed and accessible from the command
  line.
- Ensure that the paths in the script match your directory structure.
