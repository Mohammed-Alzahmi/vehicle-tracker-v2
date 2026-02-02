function enableAdminMode() {
    const checks = document.querySelectorAll('.record-check');
    const controls = document.getElementById('adminControls');
    const btn = document.getElementById('toggleAdminBtn');
    const isHidden = controls.style.display === 'none' || controls.style.display === '';
    controls.style.display = isHidden ? 'flex' : 'none';
    checks.forEach(c => c.style.display = isHidden ? 'block' : 'none');
    btn.innerText = isHidden ? 'إلغاء الإدارة' : '📑 إدارة السجلات';
}

function selectAllRecords() {
    document.querySelectorAll('.record-check').forEach(c => c.checked = true);
}

function deleteSelected() {
    const ids = Array.from(document.querySelectorAll('.record-check:checked')).map(c => c.value);
    if(ids.length === 0 || !confirm("حذف السجلات المختارة؟")) return;
    fetch("/delete-records", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({region: CURRENT_REGION, ids: ids})
    }).then(() => location.reload());
}

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
    win.document.write('<html><head><style>body{font-family:Cairo,sans-serif;text-align:center;padding:20px} iframe{display:none}</style></head><body>');
    win.document.write(content);
    win.document.write('</body></html>');
    win.document.close();
    setTimeout(() => { win.print(); win.close(); }, 500);
}

function openCarModal() { document.getElementById('carModal').style.display = 'flex'; }
function addCar() {
    const val = document.getElementById('newCarInput').value;
    if(val) manageCar('add', val);
}
function manageCar(action, value) {
    fetch("/manage-cars", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({action: action, value: value})
    }).then(() => {
        // نستخدم التحديث عشان القائمة تتغير، المودال بيتسكر بس البيانات بتنحفظ
        location.reload(); 
    });
}

function toggleMenu(region) {
    document.querySelectorAll('.menu').forEach(m => {
        if(m.id !== 'menu-'+region) m.classList.remove('show');
    });
    document.getElementById("menu-" + region).classList.toggle("show");
}