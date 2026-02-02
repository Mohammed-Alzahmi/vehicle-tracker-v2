// --- وظائف الـ Checkbox والحذف ---
function toggleAll(source) {
  checkboxes = document.querySelectorAll('.record-check');
  for(var i=0, n=checkboxes.length;i<n;i++) {
    checkboxes[i].checked = source.checked;
  }
  checkSelection();
}

function checkSelection() {
  const anyChecked = document.querySelectorAll('.record-check:checked').length > 0;
  document.getElementById('deleteBtn').style.display = anyChecked ? 'inline-block' : 'none';
}

function deleteSelected() {
  if(!confirm("هل أنت متأكد من حذف السجلات المحددة؟")) return;

  const checkboxes = document.querySelectorAll('.record-check:checked');
  const ids = Array.from(checkboxes).map(cb => cb.value);

  fetch("/delete-records", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ region: CURRENT_REGION, ids: ids })
  }).then(() => location.reload());
}

// --- وظائف إدارة السيارات ---
function openCarModal() {
  document.getElementById('carModal').style.display = 'flex';
}

function manageCar(action, value) {
  fetch("/manage-cars", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ action: action, value: value })
  }).then(res => {
    if(action === 'delete') location.reload(); // ريفرش لو حذفنا
  });
}

function addCar() {
  const val = document.getElementById('newCarInput').value;
  if(val) {
    manageCar('add', val);
    location.reload();
  }
}

// --- وظائف QR والمنيو ---
function openQR(region) {
  // الرابط يودي على صفحة register
  let link = window.location.origin + "/register/" + encodeURIComponent(region);
  document.getElementById("qrFrame").src = "https://api.qrserver.com/v1/create-qr-code/?size=250x250&data=" + link;
  document.getElementById("qrModal").style.display = "flex";
}

function closeQR(e) {
  if(e.target.id === 'qrModal') document.getElementById("qrModal").style.display = "none";
}

function toggleMenu(region) {
  // (نفس القديم)
  // ... (تأكدي ان هذا موجود في index.html لو تستخدمينه)
}



function enableAdminMode() {
    let controls = document.getElementById('adminControls');
    let checks = document.querySelectorAll('.record-check');
    let isHidden = controls.style.display === 'none' || controls.style.display === '';
    
    controls.style.display = isHidden ? 'flex' : 'none';
    checks.forEach(c => c.style.display = isHidden ? 'block' : 'none');
}

function manageCar(action, value) {
    fetch("/manage-cars", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({action: action, value: value})
    }).then(() => {
        // هنا التعديل: بدل ما نسوي ريلود للموقع كامل، نحدث القائمة بس
        // أو إذا تبين ريلود، المودال بيتسكر.. فالحل إني أشل الـ reload
        location.reload(); 
    });
}

function printQR() {
    let content = document.getElementById('printableQR').innerHTML;
    let win = window.open('', '', 'height=500,width=500');
    win.document.write('<html><body>' + content + '</body></html>');
    win.document.close();
    win.print();
}