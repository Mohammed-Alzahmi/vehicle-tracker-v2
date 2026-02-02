function toggleMenu(id) {
  const menu = document.getElementById(id);
  menu.style.display = menu.style.display === "block" ? "none" : "block";
}

function showQR() {
  document.getElementById("qrModal").style.display = "flex";
}

function closeQR() {
  document.getElementById("qrModal").style.display = "none";
}

function copyLink() {
  const link = document.getElementById("qrLink");
  navigator.clipboard.writeText(link.innerText);
  alert("Link copied ✅");
}
