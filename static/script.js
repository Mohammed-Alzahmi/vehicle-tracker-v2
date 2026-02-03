let currentOldName = "";

function toggleMenu(region, event) {
    event.stopPropagation(); // يمنع دخول الصفحة عند الضغط على النقاط
    document.querySelectorAll('.menu').forEach(m => { if(m.id !== 'menu-'+region) m.classList.remove('show'); });
    document.getElementById('menu-' + region).classList.toggle('show');
}

window.onclick = () => document.querySelectorAll('.menu').forEach(m => m.classList.remove('show'));

function deleteRegion(name, event) {
    event.stopPropagation();
    if (confirm("حذف منطقة " + name + "؟")) {
        fetch("/delete-region", { method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify({name: name}) }).then(() => location.reload());
    }
}

// وظائف التعديل الجديدة
function openEditModal(oldName, event) {
    event.stopPropagation();
    currentOldName = oldName;
    document.getElementById('editRegionInput').value = oldName;
    document.getElementById('customEditModal').style.display = 'flex';
}

function closeEditModal() {
    document.getElementById('customEditModal').style.display = 'none';
}

function saveRegionEdit() {
    let newName = document.getElementById('editRegionInput').value;
    if (newName && newName !== currentOldName) {
        fetch("/edit-region", { 
            method: "POST", 
            headers: {"Content-Type": "application/json"}, 
            body: JSON.stringify({old: currentOldName, new: newName}) 
        }).then(() => location.reload());
    } else {
        closeEditModal();
    }
}

// باقي الوظائف (إدارة السجلات والباركود)
function enableAdminMode() {
    const checks = document.querySelectorAll('.record-check');
    const controls = document.getElementById('adminControls');
    const isHidden = controls.style.display === 'none' || controls.style.display === '';
    controls.style.display = isHidden ? 'flex' : 'none';
    checks.forEach(c => c.style.display = isHidden ? 'block' : 'none');
}
function selectAllRecords() { document.querySelectorAll('.record-check').forEach(c => c.checked = true); }
function deleteSelected() {
    const ids = Array.from(document.querySelectorAll('.record-check:checked')).map(c => c.value);
    if(ids.length > 0 && confirm("حذف المحدد؟")) {
        fetch("/delete-records", { method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify({region: CURRENT_REGION, ids: ids}) }).then(() => location.reload());
    }
}
function openQR(region) {
    const url = window.location.origin + "/register/" + encodeURIComponent(region);
    document.getElementById("qrFrame").src = "https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=" + url;
    document.getElementById("qrUrlText").innerText = url;
    document.getElementById("qrModal").style.display = "flex";
}
function copyQRLink() { navigator.clipboard.writeText(document.getElementById("qrUrlText").innerText); alert("تم النسخ!"); }
function printQR() {
    const content = document.getElementById('printableQR').innerHTML;
    const win = window.open('', '', 'height=600,width=400');
    win.document.write('<html><head><style>body{font-family:Cairo;text-align:center;padding:20px} iframe{width:200px;height:200px;border:none}</style></head><body>' + content + '</body></html>');
    win.document.close();
    setTimeout(() => { win.print(); win.close(); }, 500);
}
function openCarModal() { document.getElementById('carModal').style.display = 'flex'; }
function addCar() {
    const val = document.getElementById('newCarInput').value;
    if(val) manageCar('add', val);
}
function manageCar(action, value) {
    fetch("/manage-cars", { method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify({action: action, value: value}) }).then(() => location.reload());
}