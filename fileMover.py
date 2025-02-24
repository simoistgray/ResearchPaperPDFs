import os
import re


def rename_file(old_filename):
    pattern = r'V\d+_I\d+_(.*\.pdf)'
    match = re.match(pattern, old_filename)

    if match:
        new_filename = match.group(1)
        return new_filename
    else:
        return None


def rename_files_in_directory(root_dir):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.lower().endswith('.pdf'):
                new_filename = rename_file(filename)
                if new_filename:
                    old_filepath = os.path.join(dirpath, filename)
                    new_filepath = os.path.join(dirpath, new_filename)
                    os.rename(old_filepath, new_filepath)
                    print(f"Renamed: {old_filepath} to {new_filepath}")
                else:
                    print(f"Pattern not matched for file: {filename}")


root_directory = '/pdfFolder'

rename_files_in_directory(root_directory)
