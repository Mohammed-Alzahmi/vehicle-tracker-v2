let currentOldName = "";

function toggleMenu(region) {
  let menu = document.getElementById("menu-" + region);
  // سكر أي منيو ثاني مفتوح
  document.querySelectorAll('.menu').forEach(m => {
    if(m !== menu) m.classList.remove('show');
  });
  menu.classList.toggle("show");
}

// دالة فتح مودال التعديل
function openEditModal(oldName) {
  currentOldName = oldName;
  document.getElementById("editInput").value = oldName;
  document.getElementById("editModal").style.display = "flex"; // flex عشان التوسيط
  document.getElementById("menu-" + oldName).classList.remove("show"); // سكر المنيو
}

function closeEditModal() {
  document.getElementById("editModal").style.display = "none";
}

// دالة الحفظ اليديدة
function submitEdit() {
  let newName = document.getElementById("editInput").value;
  if (!newName || newName === currentOldName) {
    closeEditModal();
    return;
  }

  fetch("/edit-region", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ old: currentOldName, new: newName })
  }).then(() => location.reload());
}

function deleteRegion(name) {
  if(!confirm("هل أنت متأكد من حذف المنطقة؟")) return;
  
  fetch("/delete-region", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name })
  }).then(() => location.reload());
}

function openQR(region) {
  // صلحنا الرابط عشان ما يعطي Not Found
  // الحين بيودي على صفحة المنطقة نفسها
  let link = window.location.origin + "/region/" + encodeURIComponent(region);
  document.getElementById("qrFrame").src = "https://api.qrserver.com/v1/create-qr-code/?size=250x250&data=" + link;
  document.getElementById("qrModal").style.display = "flex";
}

function closeQR(e) {
  if(e.target.id === 'qrModal') {
    document.getElementById("qrModal").style.display = "none";
  }
}

// سكر المنيو لو ضغطت أي مكان برا
window.onclick = function(event) {
  if (!event.target.matches('.dots')) {
    var dropdowns = document.getElementsByClassName("menu");
    for (var i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }
}