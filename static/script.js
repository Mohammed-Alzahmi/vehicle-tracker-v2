// تشغيل المنيو في الرئيسية
function toggleMenu(region, event) {
    event.stopPropagation();
    document.querySelectorAll('.menu').forEach(m => {
        if (m.id !== 'menu-' + region) m.classList.remove('show');
    });
    document.getElementById('menu-' + region).classList.toggle('show');
}

// أزرار التعديل والحذف للمناطق
function deleteRegion(name) {
    if (confirm("حذف منطقة " + name + "؟")) {
        fetch("/delete-region", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name: name })
        }).then(() => location.reload());
    }
}

function editRegion(oldName) {
    let newName = prompt("الاسم الجديد:", oldName);
    if (newName && newName !== oldName) {
        fetch("/edit-region", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ old: oldName, new: newName })
        }).then(() => location.reload());
    }
}

// إدارة السجلات (إظهار المربعات)
function enableAdminMode() {
    const checks = document.querySelectorAll('.record-check');
    const controls = document.getElementById('adminControls');
    const isHidden = controls.style.display === 'none' || controls.style.display === '';
    controls.style.display = isHidden ? 'flex' : 'none';
    checks.forEach(c => c.style.display = isHidden ? 'block' : 'none');
}

// نظام الـ QR والطباعة
function openQR(region) {
    const url = window.location.origin + "/register/" + encodeURIComponent(region);
    document.getElementById("qrFrame").src = "https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=" + url;
    document.getElementById("qrUrlText").innerText = url;
    document.getElementById("qrModal").style.display = "flex";
}

function copyQRLink() {
    navigator.clipboard.writeText(document.getElementById("qrUrlText").innerText);
    alert("تم نسخ الرابط!");
}

function printQR() {
    const content = document.getElementById('printableQR').innerHTML;
    const win = window.open('', '', 'height=600,width=400');
    win.document.write('<html><head><style>body{font-family:Cairo;text-align:center;padding:20px} iframe{width:200px;height:200px;border:none}</style></head><body>' + content + '</body></html>');
    win.document.close();
    setTimeout(() => { win.print(); win.close(); }, 500);
}

// إدارة السيارات
function addCar() {
    const val = document.getElementById('newCarInput').value;
    if(val) manageCar('add', val);
}

function manageCar(action, value) {
    fetch("/manage-cars", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({action: action, value: value})
    }).then(() => location.reload());
}