// ================================
// Small helpers
// ================================
const $ = (id) => document.getElementById(id);

function setText(el, text) {
  el.textContent = text || "";
}

function clearLater(el, ms = 2500) {
  setTimeout(() => setText(el, ""), ms);
}

function setDisabled(btn, disabled) {
  btn.disabled = !!disabled;
}

function resetProgress(bar) {
  bar.style.width = "0%";
  bar.classList.remove("indeterminate");
}

function startIndeterminate(bar) {
  bar.classList.add("indeterminate");
}

function stopIndeterminate(bar) {
  bar.classList.remove("indeterminate");
  bar.style.width = "100%";
}

// ================================
// State
// ================================
let convertFiles = [];
let mergeFiles = [];

// ================================
// Convert section elements
// ================================
const convertDrop = $("convertDrop");
const convertInput = $("convertInput");
const convertBtn = $("convertBtn");
const convertSelected = $("convertSelected");
const convertProgress = $("convertProgress");
const convertStatus = $("convertStatus");

// ================================
// Merge section elements
// ================================
const mergeDrop = $("mergeDrop");
const mergeInput = $("mergeInput");
const mergeBtn = $("mergeBtn");
const mergeSelected = $("mergeSelected");
const mergeProgress = $("mergeProgress");
const mergeStatus = $("mergeStatus");

// ================================
// Output folder path display
// ================================
async function loadOutputPath() {
  try {
    const res = await fetch("/output-info");
    const data = await res.json();
    setText($("outputPath"), data.output_folder || "output/");
  } catch {
    setText($("outputPath"), "output/");
  }
}

// ================================
// Drag & Drop utilities
// ================================
function preventDefaults(e) {
  e.preventDefault();
  e.stopPropagation();
}

function highlight(zone) {
  zone.classList.add("highlight");
}

function unhighlight(zone) {
  zone.classList.remove("highlight");
}

function setupDropzone(zone, onFiles) {
  ["dragenter", "dragover", "dragleave", "drop"].forEach((eventName) => {
    zone.addEventListener(eventName, preventDefaults, false);
  });

  ["dragenter", "dragover"].forEach((eventName) => {
    zone.addEventListener(eventName, () => highlight(zone), false);
  });

  ["dragleave", "drop"].forEach((eventName) => {
    zone.addEventListener(eventName, () => unhighlight(zone), false);
  });

  zone.addEventListener("drop", (e) => {
    const dt = e.dataTransfer;
    const files = dt ? Array.from(dt.files || []) : [];
    onFiles(files);
  });
}

// ================================
// Convert selection handling
// ================================
function setConvertFiles(files) {
  convertFiles = files.filter((f) => f && f.name && f.name.toLowerCase().endsWith(".asd"));

  if (convertFiles.length > 0) {
    setText(convertSelected, `${convertFiles.length} file(s) selected`);
    setDisabled(convertBtn, false);
  } else {
    setText(convertSelected, "");
    setDisabled(convertBtn, true);
  }

  // Clear any prior status when selection changes
  setText(convertStatus, "");
  resetProgress(convertProgress);
}

// ================================
// Merge selection handling
// ================================
function setMergeFiles(files) {
  mergeFiles = files.filter((f) => f && f.name && f.name.toLowerCase().endsWith(".csv"));

  if (mergeFiles.length > 0) {
    setText(mergeSelected, `${mergeFiles.length} file(s) selected`);
  } else {
    setText(mergeSelected, "");
  }

  // Enable merge only when 2+ CSVs
  setDisabled(mergeBtn, mergeFiles.length < 2);

  // Clear any prior status when selection changes
  setText(mergeStatus, "");
  resetProgress(mergeProgress);
}

// ================================
// Upload helpers
// ================================
async function postFiles(url, fieldName, files) {
  const form = new FormData();
  for (const f of files) form.append(fieldName, f);

  const res = await fetch(url, { method: "POST", body: form });
  const data = await res.json().catch(() => ({}));
  return { ok: res.ok, data };
}

// ================================
// Convert action
// ================================
async function doConvert() {
  if (!convertFiles.length) return;

  // UI: show progress + disable button
  setDisabled(convertBtn, true);
  startIndeterminate(convertProgress);

  // Clear selection label while processing (you wanted it to disappear)
  setText(convertSelected, "");

  const { ok, data } = await postFiles("/convert", "asd_files", convertFiles);

  stopIndeterminate(convertProgress);

  if (ok && data && data.message) {
    setText(convertStatus, data.message); // expected: "X file(s) processed successfully."
  } else {
    setText(convertStatus, (data && data.message) || (data && data.error) || "Conversion failed.");
  }

  clearLater(convertStatus, 3000);

  // Reset state after operation
  convertFiles = [];
  convertInput.value = ""; // clear chooser
  resetProgress(convertProgress);
  setDisabled(convertBtn, true);
}

// ================================
// Merge action
// ================================
async function doMerge() {
  if (mergeFiles.length < 2) return;

  setDisabled(mergeBtn, true);
  startIndeterminate(mergeProgress);

  // Clear selection label while processing
  setText(mergeSelected, "");

  const { ok, data } = await postFiles("/merge", "csv_files", mergeFiles);

  stopIndeterminate(mergeProgress);

  if (ok && data && data.message) {
    setText(mergeStatus, data.message); // expected: "X file(s) merged successfully."
  } else {
    setText(mergeStatus, (data && data.message) || (data && data.error) || "Merge failed.");
  }

  clearLater(mergeStatus, 3000);

  // Reset state after operation
  mergeFiles = [];
  mergeInput.value = "";
  resetProgress(mergeProgress);
  setDisabled(mergeBtn, true);
}

// ================================
// Wire up events
// ================================
document.addEventListener("DOMContentLoaded", () => {
  loadOutputPath();

  // Dropzones
  setupDropzone(convertDrop, (files) => setConvertFiles(files));
  setupDropzone(mergeDrop, (files) => setMergeFiles(files));

  // File inputs
  convertInput.addEventListener("change", (e) => setConvertFiles(Array.from(e.target.files || [])));
  mergeInput.addEventListener("change", (e) => setMergeFiles(Array.from(e.target.files || [])));

  // Buttons
  convertBtn.addEventListener("click", doConvert);
  mergeBtn.addEventListener("click", doMerge);

  // Initial states
  setDisabled(convertBtn, true);
  setDisabled(mergeBtn, true);
  resetProgress(convertProgress);
  resetProgress(mergeProgress);
});
