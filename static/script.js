// دوال الرئيسية (إظهار القائمة، حذف، تعديل)
function toggleMenu(id) {
    document.querySelectorAll('.menu').forEach(m => { if(m.id !== 'menu-'+id) m.style.display='none'; });
    let m = document.getElementById('menu-' + id);
    if(m) m.style.display = (m.style.display === 'block') ? 'none' : 'block';
}

function deleteRegion(name) {
    if(confirm("هل أنت متأكد من حذف منطقة " + name + "؟")) {
        fetch("/delete-region", { 
            method: "POST", headers: {"Content-Type": "application/json"}, 
            body: JSON.stringify({name: name}) 
        }).then(() => location.reload());
    }
}

let oldNameEdit = "";
function openEditModal(name) {
    oldNameEdit = name;
    document.getElementById('editInput').value = name;
    document.getElementById('editModal').style.display = 'flex';
}

function saveEdit() {
    let newN = document.getElementById('editInput').value;
    if(newN && newN !== oldNameEdit) {
        fetch("/edit-region", { 
            method: "POST", headers: {"Content-Type": "application/json"}, 
            body: JSON.stringify({old: oldNameEdit, new: newN}) 
        }).then(() => location.reload());
    }
}

// دوال صفحة التفاصيل (المركبات، الإدارة)
function toggleAdminMode() {
    let b = document.getElementById('pageBody');
    b.classList.toggle('admin-mode');
    let controls = document.getElementById('adminControls');
    controls.style.display = b.classList.contains('admin-mode') ? 'block' : 'none';
}

function manageCar(action, value) {
    fetch("/manage-cars", { 
        method: "POST", headers: {"Content-Type": "application/json"}, 
        body: JSON.stringify({region: REGION_NAME, action: action, value: value}) 
    }).then(() => location.reload());
}

function addCar() {
    let v = document.getElementById('newCarInput').value;
    if(v) manageCar('add', v);
}

function deleteSelected() {
    const ids = Array.from(document.querySelectorAll('.record-check input:checked')).map(c => c.value);
    if(ids.length > 0 && confirm("حذف السجلات المحددة؟")) {
        fetch("/delete-records", { 
            method: "POST", headers: {"Content-Type": "application/json"}, 
            body: JSON.stringify({region: REGION_NAME, ids: ids}) 
        }).then(() => location.reload());
    }
}

function selectAll() { document.querySelectorAll('.record-check input').forEach(c => c.checked = true); }
function closeModal(id) { document.getElementById(id).style.display = 'none'; }