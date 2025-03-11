from flask import Blueprint, request, jsonify
from app.services.gcs_service import upload_file_to_gcs , upload_files_to_gcs

upload_bp = Blueprint('upload', __name__)

@upload_bp.route('/upload-image', methods=['POST'])
def upload_image():
    print("helloooo", request.files)

    if 'image' not in request.files:
        return jsonify({'error': 'No file part in request'}), 400

    file_obj = request.files['image']

    if file_obj.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if not file_obj.content_type.startswith('image/'):
        return jsonify({'error': 'Uploaded file is not an image'}), 400

    try:
        image_url = upload_file_to_gcs(file_obj, folder='images')
        return jsonify({
            'message': 'Image uploaded successfully!',
            'url': image_url
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@upload_bp.route('/upload-multiple-images', methods=['POST'])
def upload_multiple_images():
    # TODO: this is for debugging purposes remove this later
    print("Received files:", request.files)
    
    # TODO: replace this with actual user_id when authentication is implemented
    user_id = "some_user_id"

    if 'images' not in request.files:
        return jsonify({'error': 'No files part in request'}), 400

    # request.files.getlist allows us to retrieve multiple files from 'images'
    files = request.files.getlist('images')

    if len(files) == 0:
        return jsonify({'error': 'No files selected'}), 400

    uploaded_images = []
    
    try:
        for file_obj in files:
            # Validate each file is an image
            if file_obj.filename == '':
                continue  # Skip empty files

            if not file_obj.content_type.startswith('image/'):
                continue  # Skip non-image files

            # Upload image (optional: pass user_id if available)
            uploaded_image = upload_file_to_gcs(file_obj,user_id, folder='images')
            
            uploaded_images.append(uploaded_image)

        if len(uploaded_images) == 0:
            return jsonify({'error': 'No valid images uploaded'}), 400

        return jsonify({
            'message': 'Images uploaded successfully!',
            'uploaded_images': uploaded_images
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500