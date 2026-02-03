// ... (الوظائف القديمة موجودة، التغيير في وظيفة الإدارة والطباعة) ...

function enableAdminMode() {
    const body = document.getElementById('pageBody');
    const checks = document.querySelectorAll('.record-check');
    const controls = document.getElementById('adminControls');
    
    const isHidden = controls.style.display === 'none' || controls.style.display === '';
    
    controls.style.display = isHidden ? 'flex' : 'none';
    checks.forEach(c => c.style.display = isHidden ? 'block' : 'none');
    
    // إضافة كلاس للجسم عشان يتحكم في توزيع الجدول
    if(isHidden) body.classList.add('admin-mode');
    else body.classList.remove('admin-mode');
}

function openQR(region) {
    const url = window.location.origin + "/register/" + encodeURIComponent(region);
    const qrImgUrl = "https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=" + url;
    document.getElementById("qrPlaceholder").innerHTML = `<img src="${qrImgUrl}" id="qrImg" style="width:200px; height:200px;">`;
    document.getElementById("qrUrlText").innerText = url;
    document.getElementById("qrModal").style.display = "flex";
}

function printQR() {
    const qrSrc = document.getElementById('qrImg').src;
    const regionName = CURRENT_REGION;
    const win = window.open('', '', 'height=600,width=400');
    win.document.write(`
        <html>
            <head>
                <style>
                    body { font-family: 'Cairo', sans-serif; text-align: center; padding-top: 50px; direction: rtl; }
                    img { width: 250px; margin-top: 20px; }
                    h1 { color: #0a2a4a; margin: 0; }
                    h2 { color: #c5a059; margin: 10px 0; }
                </style>
            </head>
            <body>
                <h1>رمز دخول المركبات</h1>
                <h2>منطقة: ${regionName}</h2>
                <img src="${qrSrc}">
                <p style="margin-top:20px; color:#666;">يرجى مسح الرمز لتسجيل الدخول</p>
            </body>
        </html>
    `);
    win.document.close();
    setTimeout(() => { win.print(); win.close(); }, 500);
}

// الباقي نفس ما هو (toggleMenu, deleteRegion, saveRegionEdit, etc.)