document.addEventListener("DOMContentLoaded", function() {
    const modal = document.getElementById("reworkModal");
    const tvModelEl = document.getElementById("modalTvModel");
    const tvSerialEl = document.getElementById("modalTvSerial");
    const defectNameEl = document.getElementById("modalDefectName");
    const defectDescEl = document.getElementById("modalDefectDesc");
    const solutionSelect = document.getElementById("solutionSelect");
    const reworkByPin = document.getElementById("rework_by_pin");
    const solutionTextEl = document.getElementById("solution_text");
    const causedByNameEl = document.getElementById("caused_by_name");
    

    let currentDefect = null;
    const token = "YOUR_JWT_TOKEN"; // JWT token

    // 🔹 Mesaj kutusu oluştur
    let msgBox = document.getElementById("error-message");
    if (!msgBox) {
        msgBox = document.createElement("div");
        msgBox.id = "submitMessage";
        msgBox.style.position = "absolute";
        msgBox.style.bottom = "20px";
        msgBox.style.left = "50%";
        msgBox.style.transform = "translateX(-50%)";
        msgBox.style.padding = "10px 20px";
        msgBox.style.borderRadius = "5px";
        msgBox.style.backgroundColor = "rgba(0,0,0,0.7)";
        msgBox.style.color = "#fff";
        msgBox.style.fontWeight = "bold";
        msgBox.style.textAlign = "center";
        msgBox.style.zIndex = "9999";
        msgBox.style.display = "none";
        modal.appendChild(msgBox);
    }

    function showMessage(msg, isError = true) {
        msgBox.textContent = msg;
        msgBox.style.backgroundColor = isError ? "rgba(220, 53, 69, 0.9)" : "rgba(25, 135, 84, 0.9)";
        msgBox.style.display = "block";
        setTimeout(() => { msgBox.style.display = "none"; }, 4000);
    }

    // 🔹 Tarih formatlama fonksiyonu
    function formatDateSafe(gmtDateStr) {
        if (!gmtDateStr) return "-";
        let date = new Date(gmtDateStr);
        if (isNaN(date)) return gmtDateStr;


        let day = String(date.getDate()).padStart(2, '0');
        let month = String(date.getMonth() + 1).padStart(2, '0');
        let year = date.getFullYear();
        let hours = String(date.getHours()).padStart(2, '0');
        let minutes = String(date.getMinutes()).padStart(2, '0');

        return `${day}/${month}/${year} ${hours}:${minutes}`;
    }

    // 🔹 Rework listesi çekme
    async function fetchReworkList() {
        try {
            const response = await fetch('/rework/list', {
                headers: { 'Authorization': 'Bearer ' + token }
            });
            const data = await response.json();

            populateTable(data.data);
        } catch(err) {
            console.error("Rework listesi alınamadı:", err);
            showMessage("Rework listesi alınamadı!", true);
        }
    }

    // 🔹 Tablonun doldurulması (yeniden kullanılabilir)
    function populateTable(items) {
        const tbody = document.querySelector('#reworkTable tbody');
        tbody.innerHTML = '';

        if(!items || !Array.isArray(items)) return;

        items.forEach(item => {
            const row = document.createElement('tr');
            row.dataset.defect = JSON.stringify(item);

            row.innerHTML = `
                <td>${item.id}</td>
                <td>${item.tv_model || '-'}</td>
                <td>${item.tv_seri_no || '-'}</td>
                <td>${item.defect_code || '-'}</td>
                <td>${item.defect_name || '-'}</td>
                <td>${item.defect_description || '-'}</td>
                <td>${item.status || '-'}</td>
                <td>${formatDateSafe(item.created_at)}</td>
                <td><button class="edit-btn">Düzenle</button></td>
            `;
            tbody.appendChild(row);
        });

        document.querySelectorAll(".edit-btn").forEach(btn => {
            btn.addEventListener("click", async function() {
                const row = btn.closest("tr");
                const defectData = JSON.parse(row.dataset.defect);
                currentDefect = defectData;

                tvModelEl.textContent = defectData.tv_model || "-";
                tvSerialEl.textContent = defectData.tv_seri_no || "-";
                defectNameEl.textContent = defectData.defect_name || "-";
                defectDescEl.textContent = defectData.defect_description || "-";

                await fetchSolutionList(defectData.id);

                reworkByPin.value = "";
                solutionTextEl.value = "";
                causedByNameEl.value = "";

                modal.style.display = "flex";
            });
        });
    }

    // 🔹 Çözüm listesini çek
    async function fetchSolutionList(defectId) {
        try {
            const res = await fetch('/solutions/list', {
                method: 'POST',
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ defect_id: defectId })
            });
            const data = await res.json();

            solutionSelect.innerHTML = "";
            if(data.data && data.data.length > 0){
                data.data.forEach(sol => {
                    const opt = document.createElement("option");
                    opt.value = sol.id;
                    opt.textContent = sol.solution_name;
                    solutionSelect.appendChild(opt);
                });
            } else {
                solutionSelect.innerHTML = '<option value="">Çözüm yok</option>';
            }

        } catch(err) {
            console.error("Çözüm listesi alınamadı:", err);
            solutionSelect.innerHTML = '<option value="">Çözüm alınamadı</option>';
            showMessage("Çözüm listesi alınamadı!", true);
        }
    }

    // 🔹 Rework submit
    window.submitRework = async function() {
        if (!currentDefect) return;

        if (!solutionSelect.value || !reworkByPin.value) {
            showMessage("Tüm zorunlu alanları doldurun!", true);
            return;
        }

        const payload = {
            defect_id: currentDefect.id,
            applied_solution_id: solutionSelect.value,
            solution_text: solutionTextEl.value,
            rework_by_pin: reworkByPin.value,
            caused_by_name: causedByNameEl.value
        };

        try {
            const res = await fetch("/rework/complete", {
                method: "POST",
                headers: {
                    "Content-Type":"application/json",
                    "Authorization": 'Bearer ' + token
                },
                body: JSON.stringify(payload)
            });

            const data = await res.json();

            if(res.ok){
                showMessage(data.message || "Rework başarıyla tamamlandı!", false);
                fetchReworkList();
                modal.style.display = "none";
            } else {
                showMessage((data.message || "Rework tamamlanamadı!") + (data.error ? " | " + data.error : ""), true);
            }

        } catch(err) {
            console.error(err);
            showMessage("Rework tamamlanamadı!", true);
        }
    };

    // 🔹 Tablo filtreleme
    window.filterTable = function() {
        const input = document.getElementById('search').value.toLowerCase();
        const table = document.getElementById('reworkTable');
        Array.from(table.getElementsByTagName('tr')).forEach((tr,i)=>{
            if(i===0) return;
            const rowText = tr.textContent.toLowerCase();
            tr.style.display = rowText.includes(input) ? '' : 'none';
        });
    };

    // 🔹 Modal kapatma
    document.getElementById("closeReworkBtn").addEventListener("click", () => {
        modal.style.display = "none";
    });

    // 🔹 Tümünü Listele butonu
    // 🔹 Tümünü Listele butonu - yeni sayfaya yönlendir
    const listAllBtn = document.getElementById("listAllBtn");
    if(listAllBtn){
        listAllBtn.addEventListener("click", () => {
            window.location.href = '/defect/list/all';
        });

            document.getElementById("backButton").addEventListener("click", () => {
    window.history.back(); // bir önceki sayfaya döner
});

    }


    fetchReworkList();
});
