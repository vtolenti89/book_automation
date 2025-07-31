let svgFiles = [];

document.getElementById("svgFiles").addEventListener("change", (event) => {
  svgFiles = Array.from(event.target.files);
});

document.getElementById("analyzeColors").addEventListener("click", async () => {
  if (svgFiles.length === 0) {
    alert("Please select one or more SVG files first.");
    return;
  }

  const colorSet = new Set();

  for (const file of svgFiles) {
    const text = await file.text();
    const matches = text.match(/fill:\s*#([0-9a-fA-F]{6})/g) || [];

    matches.forEach((match) => {
      const color = match.split(":")[1].trim().toLowerCase();
      colorSet.add(color);
    });
  }

  const container = document.getElementById("colorMappings");
  container.innerHTML = "";

  colorSet.forEach((color, index) => {
    const div = document.createElement("div");
    div.classList.add("d-flex", "align-items-center", "mb-2");

    const oldColorInput = document.createElement("input");
    oldColorInput.value = color;
    oldColorInput.disabled = true;
    oldColorInput.style.backgroundColor = color;
    oldColorInput.classList.add("form-control", "me-2");
    oldColorInput.style.width = "150px";

    const newColorInput = document.createElement("input");
    newColorInput.type = "color";
    newColorInput.value = color;
    newColorInput.classList.add("form-control");
    newColorInput.style.width = "60px";
    newColorInput.dataset.oldColor = color;

    div.appendChild(oldColorInput);
    div.appendChild(newColorInput);
    container.appendChild(div);
  });

  document.getElementById("applyColorChanges").style.display = "block";
});

document.getElementById("previewColorChanges").addEventListener("click", async () => {
  const mappings = {};
  const colorInputs = document.querySelectorAll("#colorMappings input[type='color']");
  colorInputs.forEach((input) => {
    const oldColor = input.dataset.oldColor;
    const newColor = input.value.toLowerCase();
    mappings[oldColor] = newColor;
  });

  const formData = new FormData();
  const filenames = [];

  svgFiles.forEach((file) => {
    filenames.push(file.name);
    formData.append("svg_files", file);
  });
  formData.append("color_map", JSON.stringify(mappings));

  const res = await fetch("/api/sla/preview-svg-colors", {
    method: "POST",
    body: formData,
  });

  const result = await res.json();
  alert(result.message || "Preview generated.");

  // Render previews
  const previewContainer = document.getElementById("svgPreviewContainer");
  previewContainer.innerHTML = "";

  filenames.forEach(filename => {
    const wrapper = document.createElement("div");
    wrapper.classList.add("d-flex", "flex-column", "align-items-center", "mb-4");

    const img = document.createElement("img");
    img.src = `/static/preview/${filename}?t=${Date.now()}`;
    img.alt = filename;
    img.style.maxWidth = "200px";
    img.style.cursor = "pointer";
    img.classList.add("mb-2", "border");

    img.addEventListener("click", () => {
      document.getElementById("modalOriginal").src = `/static/preview/original_${filename}`;
      document.getElementById("modalModified").src = `/static/preview/${filename}?t=${Date.now()}`;
      const modal = new bootstrap.Modal(document.getElementById("svgModal"));
      modal.show();
    });

    wrapper.appendChild(img);
    previewContainer.appendChild(wrapper);
  });

  // Enable apply button
  document.getElementById("applyColorChanges").disabled = false;
});



document.getElementById("applyColorChanges").addEventListener("click", async () => {
  const res = await fetch("/api/sla/apply-svg-color-changes", {
    method: "POST"
  });

  const result = await res.json();
  alert(result.message || "SVG files updated.");

  // Optionally disable apply button again
  document.getElementById("applyColorChanges").disabled = true;
});

