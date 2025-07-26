from flask import Blueprint, request, jsonify
from app.services.sla_service import replace_color, move_svg_picture, preview

sla_bp = Blueprint('sla_editor', __name__)

@sla_bp.route('/replace-color', methods=['POST'])
def replace_color_api():
    data = request.json
    result = replace_color(data['file_path'], data['target_color'], data['replacement_color'])
    return jsonify({"success": result})

@sla_bp.route('/move-picture', methods=['POST'])
def move_picture_api():
    data = request.json
    result = move_svg_picture(data['file_path'], data['image_name'], data['dx'], data['dy'])
    return jsonify({"success": result})

@sla_bp.route('/preview', methods=['POST'])
def preview_api():
    data = request.json
    result = preview(data['file_path'])
    return jsonify(result)
