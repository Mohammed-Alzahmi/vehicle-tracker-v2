function toggleMenu(id){
  document.getElementById("menu-"+id).classList.toggle("show");
}

function showQR(link){
  document.getElementById("qrModal").style.display="block";
  document.getElementById("qrImage").src =
    "https://api.qrserver.com/v1/create-qr-code/?size=250x250&data="+link;
  window.qrLink = link;
}

function closeQR(){
  document.getElementById("qrModal").style.display="none";
}

function copyLink(){
  navigator.clipboard.writeText(window.qrLink);
  alert("تم النسخ");
}
