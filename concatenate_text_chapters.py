import os
import glob


def concatenate_files(directory_path="./ebook_text_files"):
    # Ensure the directory exists
    if not os.path.exists(directory_path):
        print(f"Directory {directory_path} does not exist.")
        return

    # Initialize an empty string to store the concatenated text
    concatenated_text = ""

    # Sort files so that split files (e.g., part0011_split_000.html, part0011_split_001.html) are processed together
    all_files = sorted(glob.glob(os.path.join(directory_path, "*.html")))

    for file_path in all_files:
        with open(file_path, "r", encoding="utf-8") as file:
            concatenated_text += file.read()

    # Save the concatenated text to a new HTML file
    output_file_path = os.path.join(directory_path, "concatenated_ebook.html")
    with open(output_file_path, "w", encoding="utf-8") as output_file:
        output_file.write(concatenated_text)

    print(f"Concatenation complete. Output saved to {output_file_path}")


if __name__ == "__main__":
    concatenate_files()
