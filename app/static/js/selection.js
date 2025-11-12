// Protected veri kontrolü (JWT cookie ile)
window.addEventListener('DOMContentLoaded', () => {
    fetch('/process/selection', {
        method: 'GET',
        credentials: 'include'
    })
    .then(res => {
        if (res.status === 401) {
            window.location.href = '/auth';
        }
    })
    .catch(err => console.error(err));
});

    document.getElementById("backButton").addEventListener("click", () => {
    window.history.back(); // bir önceki sayfaya döner
});



