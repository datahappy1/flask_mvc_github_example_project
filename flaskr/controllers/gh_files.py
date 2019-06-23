from flask import session, flash


def put_file(file_content, branch_name):
    f = file_content
    session['file_upload_contents'] = f
    flash(f.filename + ' stored!')
