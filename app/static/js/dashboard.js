// Kullanıcı verisi (backend yerine simülasyon)
const userData = {
    user_name: "John Doe",
    user_title: "D. in Medicine"
};

document.getElementById("user_name").textContent = userData.user_name;
document.getElementById("user_title").textContent = userData.user_title;

// Gece modu toggle (opsiyonel)
const toggle = document.getElementById("nightToggle");
if(toggle){
    toggle.addEventListener("change", () => {
        document.body.classList.toggle("night-mode");
    });
}
