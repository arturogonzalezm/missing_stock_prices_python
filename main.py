from src.comparison import main

if __name__ == '__main__':
    result = main()
    if result is not None:
        print(result)


# import os
#
#
# def print_directory_tree(startpath, ignore=None):
#     ignore = set(ignore or [])
#     for root, dirs, files in os.walk(startpath, topdown=True):
#         dirs[:] = [d for d in dirs if d not in ignore]  # Modify dirs in-place to ignore specified directories
#         level = root.replace(startpath, '').count(os.sep)
#         indent = ' ' * 4 * (level)
#         print(f"{indent}{os.path.basename(root)}/")
#         subindent = ' ' * 4 * (level + 1)
#         for f in files:
#             print(f"{subindent}{f}")
#
#
# if __name__ == "__main__":
#     project_root = input("Enter the path to the Python project: ")
#     ignore_folders = input("Enter folder names to ignore separated by commas (e.g., env, .git): ")
#     ignore_list = [x.strip() for x in ignore_folders.split(',')] if ignore_folders else []
#     print_directory_tree(project_root, ignore=ignore_list)
