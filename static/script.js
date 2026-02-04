let currentOldName = "";
function toggleMenu(id) { 
    let m = document.getElementById('menu-' + id);
    m.style.display = (m.style.display === 'none') ? 'block' : 'none';
}
function openEditModal(name) {
    currentOldName = name;
    document.getElementById('editInput').value = name;
    document.getElementById('editModal').style.display = 'flex';
}
function saveEdit() {
    let newName = document.getElementById('editInput').value;
    if(newName && newName !== currentOldName) {
        fetch("/edit-region", { method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify({old: currentOldName, new: newName}) }).then(() => location.reload());
    }
}
function deleteRegion(name) {
    if(confirm("حذف " + name + "؟")) {
        fetch("/delete-region", { method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify({name: name}) }).then(() => location.reload());
    }
}
function toggleAdminMode() {
    const body = document.getElementById('pageBody');
    const controls = document.getElementById('adminControls');
    body.classList.toggle('admin-mode');
    controls.style.display = body.classList.contains('admin-mode') ? 'block' : 'none';
}
function selectAll() { document.querySelectorAll('.record-check').forEach(c => c.checked = true); }
function deleteSelected() {
    const ids = Array.from(document.querySelectorAll('.record-check:checked')).map(c => c.value);
    if(ids.length > 0 && confirm("حذف المحدده؟")) {
        fetch("/delete-records", { method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify({region: REGION_NAME, ids: ids}) }).then(() => location.reload());
    }
}
function showQR() {
    const url = window.location.origin + "/register/" + encodeURIComponent(REGION_NAME);
    document.getElementById('qrContainer').innerHTML = `<img src="https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=${url}" id="qrImg" style="width:200px;">`;
    document.getElementById('qrLinkText').innerText = url;
    document.getElementById('qrModal').style.display = 'flex';
}
function printQR() {
    const qrSrc = document.getElementById('qrImg').src;
    const win = window.open('', '', 'height=600,width=400');
    win.document.write(`<html><head><style>body{font-family:'Cairo';text-align:center;padding:40px;direction:rtl} h1{color:#0a2a4a} h2{color:#c5a059} img{width:250px;margin-top:20px}</style></head><body><h1>رمز دخول المركبات</h1><h2>منطقة: ${REGION_NAME}</h2><img src="${qrSrc}"><p style="margin-top:30px;color:#888">نظام إدارة السجلات الرقمي</p></body></html>`);
    win.document.close();
    setTimeout(() => { win.print(); win.close(); }, 500);
}
function closeModal(id) { document.getElementById(id).style.display = 'none'; }
function copyLink() { navigator.clipboard.writeText(document.getElementById('qrLinkText').innerText); alert("تم النسخ"); }
function openCarModal() { document.getElementById('carModal').style.display = 'flex'; }
function addCar() {
    const val = document.getElementById('newCarInput').value;
    if(val) manageCar('add', val);
}
function manageCar(action, value) {
    fetch("/manage-cars", { method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify({action: action, value: value}) }).then(() => location.reload());
}