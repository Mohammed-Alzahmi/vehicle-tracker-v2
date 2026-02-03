function enableAdminMode() {
    const body = document.getElementById('pageBody');
    const controls = document.getElementById('adminControls');
    const checks = document.querySelectorAll('.record-check');
    
    const isActive = body.classList.toggle('admin-mode');
    controls.style.display = isActive ? 'flex' : 'none';
    checks.forEach(c => c.style.display = isActive ? 'block' : 'none');
}

function openQR(region) {
    const url = window.location.origin + "/register/" + encodeURIComponent(region);
    const qrImgUrl = "https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=" + url;
    document.getElementById("qrPlaceholder").innerHTML = `<img src="${qrImgUrl}" id="qrImg" style="width:200px;">`;
    document.getElementById("qrUrlText").innerText = url;
    document.getElementById("qrModal").style.display = "flex";
}

function printQR() {
    window.print(); // بيطبع الباركود والاسم بس لأننا عدلنا الـ CSS @media print
}

// دالة تحديد الكل
function selectAllRecords() {
    const checks = document.querySelectorAll('.record-check');
    const allChecked = Array.from(checks).every(c => c.checked);
    checks.forEach(c => c.checked = !allChecked);
}