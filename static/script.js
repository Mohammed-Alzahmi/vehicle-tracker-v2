// دوال الرئيسية
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

// === التعديل الجديد للمركبات (بدون ريفريش) ===
function addCarDirect() {
    let input = document.getElementById('newCarInput');
    let value = input.value;
    if(!value) return;

    fetch("/manage-cars", { 
        method: "POST", headers: {"Content-Type": "application/json"}, 
        body: JSON.stringify({region: REGION_NAME, action: "add", value: value}) 
    }).then(res => res.json()).then(data => {
        if(data.success) {
            // إضافة العنصر للقائمة فوراً بدون تحديث الصفحة
            let list = document.getElementById('carList');
            let newItem = document.createElement('div');
            let randomId = 'new-' + Date.now();
            newItem.className = 'car-item';
            newItem.id = randomId;
            newItem.innerHTML = `<span>${value}</span><span onclick="deleteCarDirect('${value}', '${randomId}')" style="color:red; cursor:pointer; font-weight:bold;">🗑️</span>`;
            list.appendChild(newItem);
            input.value = ""; // تفريغ الخانة
        }
    });
}

function deleteCarDirect(carName, elementId) {
    fetch("/manage-cars", { 
        method: "POST", headers: {"Content-Type": "application/json"}, 
        body: JSON.stringify({region: REGION_NAME, action: "delete", value: carName}) 
    }).then(res => res.json()).then(data => {
        if(data.success) {
            // حذف العنصر من الشاشة فوراً
            document.getElementById(elementId).remove();
        }
    });
}

// دوال إدارة السجلات
function toggleAdminMode() {
    let b = document.getElementById('pageBody');
    b.classList.toggle('admin-mode');
    let controls = document.getElementById('adminControls');
    controls.style.display = b.classList.contains('admin-mode') ? 'block' : 'none';
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