from pathlib import Path
import shutil


def delete_student_files(name, roll_number):
    """
    Deletes a student's image folder and encoding file.
    """

    folder = Path("images") / f"{name}_{roll_number}"

    if folder.exists():
        shutil.rmtree(folder)

    encoding = Path("encodings") / f"{name}_{roll_number}.npy"

    if encoding.exists():
        encoding.unlink()


def rename_student_files(old_name, old_roll, new_name, new_roll):
    """
    Renames the student's image folder and encoding file.
    """

    # ----------------------------
    # Rename image folder
    # ----------------------------

    old_folder = Path("images") / f"{old_name}_{old_roll}"
    new_folder = Path("images") / f"{new_name}_{new_roll}"

    if old_folder.exists():
        old_folder.rename(new_folder)

    # ----------------------------
    # Rename encoding file
    # ----------------------------

    old_encoding = Path("encodings") / f"{old_name}_{old_roll}.npy"
    new_encoding = Path("encodings") / f"{new_name}_{new_roll}.npy"

    if old_encoding.exists():
        old_encoding.rename(new_encoding)

