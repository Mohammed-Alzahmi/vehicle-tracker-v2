function toggleMenu(region, event) {
    event.stopPropagation();
    document.querySelectorAll('.menu').forEach(m => {
        if (m.id !== 'menu-' + region) m.classList.remove('show');
    });
    document.getElementById('menu-' + region).classList.toggle('show');
}

// إغلاق المنيو عند الضغط في أي مكان
window.onclick = function() {
    document.querySelectorAll('.menu').forEach(m => m.classList.remove('show'));
}

function deleteRegion(name) {
    if (confirm("هل أنت متأكد من حذف منطقة " + name + " وكل سجلاتها؟")) {
        fetch("/delete-region", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name: name })
        }).then(() => location.reload());
    }
}

function editRegion(oldName) {
    let newName = prompt("أدخل الاسم الجديد للمنطقة:", oldName);
    if (newName && newName !== oldName) {
        fetch("/edit-region", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ old: oldName, new: newName })
        }).then(() => location.reload());
    }
}