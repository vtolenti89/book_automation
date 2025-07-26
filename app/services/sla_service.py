from lxml import etree

def replace_color(file_path, target_color, replacement_color):
    tree = etree.parse(file_path)
    root = tree.getroot()

    changed = False
    for elem in root.iter():
        if elem.get("FillColor") == target_color:
            elem.set("FillColor", replacement_color)
            changed = True

    if changed:
        tree.write(file_path, pretty_print=True)
    return changed

def move_svg_picture(file_path, image_name, dx, dy):
    tree = etree.parse(file_path)
    root = tree.getroot()
    moved = False

    for elem in root.iter("Image"):
        if elem.get("PFILE") and image_name in elem.get("PFILE"):
            try:
                x = float(elem.get("XPOS"))
                y = float(elem.get("YPOS"))
                elem.set("XPOS", str(x + dx))
                elem.set("YPOS", str(y + dy))
                moved = True
            except:
                continue

    if moved:
        tree.write(file_path, pretty_print=True)
    return moved

def preview(file_path):
    # Dummy version – real version could convert SLA to PNG/PDF using Scribus CLI
    return {"preview_url": "/static/previews/preview.png"}
