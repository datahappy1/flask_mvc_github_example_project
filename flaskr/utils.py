"""
utils.py
"""
import os
from werkzeug.utils import secure_filename


def file_uploader_helper(file) -> tuple:
    """
    file upload helper function
    :param file:
    :return:
    """
    temp_folder = os.path.join(os.getcwd(), 'temp')
    if not os.path.isdir(temp_folder):
        try:
            os.mkdir(temp_folder)
        except OSError:
            raise OSError(f'Cannot create temp folder {temp_folder}')

    file_name = secure_filename(file.filename)
    temp_file_path = os.path.join(temp_folder, file_name)

    file.save(temp_file_path)
    with open(temp_file_path, 'rb') as temp_file_handler:
        file_contents = temp_file_handler.read()

    os.unlink(temp_file_path)
    assert not os.path.exists(temp_file_path)

    return file_name, file_contents
