const preview = document.getElementById("preview");
const result = document.getElementById("result");

document.getElementById("imageInput").addEventListener("change", function () {
  const file = this.files[0];
  if (file) {
    preview.src = URL.createObjectURL(file);
    preview.hidden = false;
    result.innerText = "";
  }
});

async function upload() {
  const input = document.getElementById('imageInput');
  const file = input.files[0];
  if (!file) return alert("Please choose an image first!");

  const formData = new FormData();
  formData.append("file", file);
  result.innerText = "⏳ Predicting...";

  try {
    const res = await fetch("http://127.0.0.1:8000/predict", {
      method: "POST",
      body: formData
    });
    const data = await res.json();
    result.innerHTML = `
      <span class="emoji">✅</span>Prediction: <strong>${data.prediction.toUpperCase()}</strong><br>
      <span class="emoji">🧾</span>Confidence: <strong>${data.confidence}%</strong>
    `;

  } catch (err) {
    console.error(err);
    result.innerText = "❌ Prediction failed. See console.";
  }
}
