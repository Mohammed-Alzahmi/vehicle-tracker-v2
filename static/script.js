// دالة فتح وإغلاق المنيو في الرئيسية
function toggleMenu(id) {
    document.querySelectorAll('.menu').forEach(m => { if(m.id !== 'menu-'+id) m.style.display = 'none'; });
    let m = document.getElementById('menu-' + id);
    m.style.display = (m.style.display === 'none' || m.style.display === '') ? 'block' : 'none';
}

// تعديل اسم المنطقة
let currentEditOldName = "";
function openEditModal(name) {
    currentEditOldName = name;
    document.getElementById('editInput').value = name;
    document.getElementById('editModal').style.display = 'flex';
}
function saveEdit() {
    let newName = document.getElementById('editInput').value;
    if(newName && newName !== currentEditOldName) {
        fetch("/edit-region", { 
            method: "POST", 
            headers: {"Content-Type": "application/json"}, 
            body: JSON.stringify({old: currentEditOldName, new: newName}) 
        }).then(() => window.location.reload());
    }
}

// حذف المنطقة
function deleteRegion(name) {
    if(confirm("هل أنت متأكد من حذف منطقة: " + name + "؟")) {
        fetch("/delete-region", { 
            method: "POST", 
            headers: {"Content-Type": "application/json"}, 
            body: JSON.stringify({name: name}) 
        }).then(() => window.location.reload());
    }
}

// إدارة المركبات (إضافة وحذف)
function manageCar(action, value) {
    fetch("/manage-cars", { 
        method: "POST", 
        headers: {"Content-Type": "application/json"}, 
        body: JSON.stringify({region: REGION_NAME, action: action, value: value}) 
    }).then(res => res.json()).then(data => {
        if(data.success) window.location.reload();
    });
}

function addCar() {
    const val = document.getElementById('newCarInput').value;
    if(val) manageCar('add', val);
}

// وظائف عامة
function closeModal(id) { document.getElementById(id).style.display = 'none'; }
function toggleAdminMode() { 
    const body = document.getElementById('pageBody');
    body.classList.toggle('admin-mode');
    document.getElementById('adminControls').style.display = body.classList.contains('admin-mode') ? 'block' : 'none';
}
function selectAll() { document.querySelectorAll('.record-check').forEach(c => c.checked = true); }
function deleteSelected() {
    const ids = Array.from(document.querySelectorAll('.record-check:checked')).map(c => c.value);
    if(ids.length > 0 && confirm("حذف السجلات المختارة؟")) {
        fetch("/delete-records", { 
            method: "POST", 
            headers: {"Content-Type": "application/json"}, 
            body: JSON.stringify({region: REGION_NAME, ids: ids}) 
        }).then(() => window.location.reload());
    }
}