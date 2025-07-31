from flask import Blueprint, request, jsonify
from app.services.svg_service import replace_svg_colors
from werkzeug.utils import secure_filename
import json
import os

sla_bp = Blueprint('sla_editor', __name__)

@sla_bp.route('/preview-svg-colors', methods=['POST'])
def preview_svg_colors_api():
    files = request.files.getlist("svg_files")
    color_map = request.form.get("color_map")
    if not files or not color_map:
        return jsonify({"error": "Missing files or color mapping"}), 400

    import json
    color_map = json.loads(color_map)

    os.makedirs("static/preview", exist_ok=True)

    for file in files:
        filename = secure_filename(file.filename)
        svg_text = file.read().decode("utf-8")

        # Save original for side-by-side
        with open(f"./static/preview/original_{filename}", "w", encoding="utf-8") as f:
            f.write(svg_text)

        # Generate modified preview version
        from app.services.svg_service import replace_svg_colors
        modified_svg = replace_svg_colors(svg_text, color_map)

        with open(f"./static/preview/{filename}", "w", encoding="utf-8") as f:
            f.write(modified_svg)

    # Save the mapping globally for Apply step (simplified for now)
    with open("color_session.json", "w") as f:
        json.dump({
            "color_map": color_map,
            "filenames": [secure_filename(file.filename) for file in files]
        }, f)

    return jsonify({"message": "Preview ready."})


@sla_bp.route('/apply-svg-color-changes', methods=['POST'])
def apply_svg_color_changes():
    import json

    try:
        with open("color_session.json", "r") as f:
            session = json.load(f)
    except FileNotFoundError:
        return jsonify({"error": "No preview session found."}), 400

    filenames = session["filenames"]
    color_map = session["color_map"]

    os.makedirs("static/processed", exist_ok=True)

    updated = 0
    for filename in filenames:
        path = f"./static/preview/original_{filename}"
        if not os.path.exists(path):
            continue

        with open(path, "r", encoding="utf-8") as f:
            svg_text = f.read()

        from app.services.svg_service import replace_svg_colors
        modified_svg = replace_svg_colors(svg_text, color_map)

        with open(f"./static/processed/{filename}", "w", encoding="utf-8") as f:
            f.write(modified_svg)

        updated += 1

    return jsonify({"message": f"{updated} original files modified."})
