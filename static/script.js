// دوال المنيو والحذف في الرئيسية
function toggleMenu(id) {
    document.querySelectorAll('.menu').forEach(m => { if(m.id !== 'menu-'+id) m.style.display='none'; });
    let m = document.getElementById('menu-' + id);
    m.style.display = (m.style.display === 'block') ? 'none' : 'block';
}

function deleteRegion(name) {
    if(confirm("حذف منطقة " + name + "؟")) {
        fetch("/delete-region", { method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify({name: name}) }).then(() => location.reload());
    }
}

let oldNameForEdit = "";
function openEditModal(name) {
    oldNameForEdit = name;
    document.getElementById('editInput').value = name;
    document.getElementById('editModal').style.display = 'flex';
}
function saveEdit() {
    let newN = document.getElementById('editInput').value;
    if(newN && newN !== oldNameForEdit) {
        fetch("/edit-region", { method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify({old: oldNameForEdit, new: newN}) }).then(() => location.reload());
    }
}

// دوال الريجن والسيارات
function manageCar(action, value) {
    fetch("/manage-cars", { method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify({region: REGION_NAME, action: action, value: value}) }).then(() => location.reload());
}
function addCar() {
    let v = document.getElementById('newCarInput').value;
    if(v) manageCar('add', v);
}
function toggleAdminMode() {
    let b = document.getElementById('pageBody');
    b.classList.toggle('admin-mode');
    document.getElementById('adminControls').style.display = b.classList.contains('admin-mode') ? 'block' : 'none';
}
function closeModal(id) { document.getElementById(id).style.display = 'none'; }