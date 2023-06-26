import filecmp
import fileinput
import os

def compare_files(file_path1, file_path2):
    """
    Compare two files and print the differences, if any.

    Args:
        file_path1 (str): Path to the first file.
        file_path2 (str): Path to the second file.

    Returns:
        bool: True if the files are identical, False otherwise.
    """
    with open(file_path1, 'r', encoding='utf-8', errors='replace') as file1, \
            open(file_path2, 'r', encoding='utf-8', errors='replace') as file2:
        lines1 = [line.strip() for line in file1]
        lines2 = [line.strip() for line in file2]

        if len(lines1) != len(lines2):
            print(f"Difference in file: {file_path1}")
            return False

        for i, (line1, line2) in enumerate(zip(lines1, lines2)):
            for j, (char1, char2) in enumerate(zip(line1, line2)):
                if char1 != char2:
                    print(f"Difference in file: {file_path1}")
                    print(f"Line {i+1}, Char {j+1}:")
                    print(f"- {line1}")
                    print(f"- {char1}")
                    print(f"+ {line2}")
                    print(f"+ {char2}")
                    return False

    return True
        

def compare_folders(folder_path1, folder_path2):
    """
    Compare two folders and print the differences, if any.

    Args:
        folder_path1 (str): Path to the first folder.
        folder_path2 (str): Path to the second folder.

    Returns:
        bool: True if the folders are identical, False otherwise.
    """
    comparison = filecmp.dircmp(folder_path1, folder_path2)

    if comparison.left_only or comparison.right_only or comparison.diff_files:
        if comparison.left_only:
            print("Files only in left folder:")
            for file in comparison.left_only:
                print(os.path.join(folder_path1, file))

        if comparison.right_only:
            print("Files only in right folder:")
            for file in comparison.right_only:
                print(os.path.join(folder_path2, file))

        if comparison.diff_files:
            print("Differing files:")
            for file in comparison.diff_files:
                file_path1 = os.path.join(folder_path1, file)
                file_path2 = os.path.join(folder_path2, file)
                compare_files(file_path1, file_path2)
    else:
        for common_file in comparison.common_files:
            file_path1 = os.path.join(folder_path1, common_file)
            file_path2 = os.path.join(folder_path2, common_file)
            if not compare_files(file_path1, file_path2):
                return False
        for subdir in comparison.common_dirs:
            new_folder_path1 = os.path.join(folder_path1, subdir)
            new_folder_path2 = os.path.join(folder_path2, subdir)
            if not compare_folders(new_folder_path1, new_folder_path2):
                return False
    return True

# Example usage:
folder_path1 = 'E:\\test\\projects1'
folder_path2 = 'E:\\test\\projects2'

if compare_folders(folder_path1, folder_path2):
    print("The folders are identical.")
else:
    print("The folders are not identical.")