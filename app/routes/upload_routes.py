from flask import Blueprint, request, jsonify
from app.services.gcs_service import upload_file_to_gcs
from app.utils.decorators import token_required

upload_bp = Blueprint('upload', __name__)

# Single Image Upload - User must be authenticated
@upload_bp.route('/upload-image', methods=['POST'])
@token_required
def upload_image():
    current_user = request.user  # Added user context here
    user_id = current_user['user_id']  # You can now use the user's ID

    if 'image' not in request.files:
        return jsonify({'error': 'No file part in request'}), 400

    file_obj = request.files['image']

    if file_obj.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if not file_obj.content_type.startswith('image/'):
        return jsonify({'error': 'Uploaded file is not an image'}), 400

    try:
        # Upload file to GCS, passing user_id if needed in your gcs_service
        image_url = upload_file_to_gcs(file_obj, user_id=user_id, folder='images')

        return jsonify({
            'message': 'Image uploaded successfully!',
            'url': image_url
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Multiple Images Upload - User must be authenticated
@upload_bp.route('/upload-multiple-images', methods=['POST'])
@token_required
def upload_multiple_images():
    current_user = request.user
    user_id = current_user['user_id']

    if 'images' not in request.files:
        return jsonify({'error': 'No files part in request'}), 400

    files = request.files.getlist('images')

    if len(files) == 0:
        return jsonify({'error': 'No files selected'}), 400

    uploaded_images = []

    try:
        for file_obj in files:
            if file_obj.filename == '':
                continue  # Skip empty files

            if not file_obj.content_type.startswith('image/'):
                continue  # Skip non-image files

            uploaded_image = upload_file_to_gcs(file_obj, user_id=user_id, folder='images')

            uploaded_images.append(uploaded_image)

        if len(uploaded_images) == 0:
            return jsonify({'error': 'No valid images uploaded'}), 400

        return jsonify({
            'message': 'Images uploaded successfully!',
            'uploaded_images': uploaded_images
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500