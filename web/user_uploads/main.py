import os
from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from denoising.enhancer import enhance_image

bp = Blueprint('main', __name__)

@bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['dicom_file']
        if file:
            filename = secure_filename(file.filename)
            upload_path = os.path.join('web/uploads', filename)
            file.save(upload_path)

            # Process the DICOM image
            output_path = enhance_image(upload_path)

            return render_template('result.html', image_file='enhanced.png')
    return render_template('index.html')
