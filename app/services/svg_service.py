import re

def replace_svg_colors(svg_content: str, color_map: dict) -> str:
    # Normalize color map (e.g., '#832323' -> '832323')
    normalized_map = {k.lstrip('#').lower(): v.lower() for k, v in color_map.items()}

    # Regex to catch fill colors in both direct and style usage
    def replace_match(match):
        original = match.group(0)
        color = match.group(1).lower()
        new_color = normalized_map.get(color, f"#{color}")
        return original.replace(f"#{color}", new_color)

    # Match things like fill:#832323 or style="fill:#832323"
    return re.sub(r"#([0-9a-fA-F]{6})", replace_match, svg_content)
