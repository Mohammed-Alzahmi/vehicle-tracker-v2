function toggleMenu(region) {
  document.getElementById("menu-" + region).classList.toggle("show");
}

function deleteRegion(name) {
  fetch("/delete-region", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name })
  }).then(() => location.reload());
}

function editRegion(oldName) {
  let newName = prompt("New region name:");
  if (!newName) return;

  fetch("/edit-region", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ old: oldName, new: newName })
  }).then(() => location.reload());
}

function openQR(region) {
  document.getElementById("qrFrame").src = "/qr/" + region;
  document.getElementById("qrModal").style.display = "block";
}
