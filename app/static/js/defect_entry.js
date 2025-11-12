document.addEventListener("DOMContentLoaded", () => {

    const defectSelect = document.getElementById("defect_select");
    const defectTagsContainer = document.getElementById("defect-tags");
    const form = document.getElementById("defectEntryForm");
    let addedDefects = []; // eklenen hataları tutar

    // 🔹 Select kutusunda yazı rengini değiştir
    defectSelect.addEventListener("change", () => {
        defectSelect.style.color = defectSelect.value ? "#fff" : "#aaa";
    });

    // 🔹 Hata listesini backend’den al
    fetch("/catalog", { credentials: "include" })
        .then(res => res.json())
        .then(data => {
            data.forEach(d => {
                const option = document.createElement("option");
                option.value = d.id;
                option.text = d.defect_name;
                defectSelect.appendChild(option);
            });
        })
        .catch(err => console.error("Hata listesi alınamadı:", err));

    // 🔹 Hata ekleme butonu
    document.getElementById("addDefectBtn").addEventListener("click", () => {
        const selectedId = defectSelect.value;
        const selectedText = defectSelect.options[defectSelect.selectedIndex].text;
        if (!selectedId) return;
        if (addedDefects.some(d => d.id === selectedId)) return;

        addedDefects.push({ id: selectedId, name: selectedText });
        renderDefectTags();
    });

    function renderDefectTags() {
        defectTagsContainer.innerHTML = "";
        addedDefects.forEach(d => {
            const tag = document.createElement("div");
            tag.className = "defect-tag";
            tag.innerHTML = `${d.name} <span class="remove-tag">&times;</span>`;
            tag.querySelector(".remove-tag").addEventListener("click", () => {
                addedDefects = addedDefects.filter(x => x.id !== d.id);
                renderDefectTags();
            });
            defectTagsContainer.appendChild(tag);
        });
    }

    // 🔹 Durum butonları
    const situationButtons = document.querySelectorAll(".situation-buttons button");
    let selectedSituation = null;

    situationButtons.forEach(btn => {
        btn.addEventListener("click", () => {
            situationButtons.forEach(b => b.classList.remove("active"));
            btn.classList.add("active");
            selectedSituation = btn.getAttribute("data-value");
        });
    });

    // 🔹 Geri butonu
    document.getElementById("backBtn").addEventListener("click", () => window.history.back());

    // 🔹 Form gönderme
    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const tvSerial = document.getElementById("tv_serial").value.trim();
        const pin = document.getElementById("pin").value.trim();

        if (!tvSerial || addedDefects.length === 0 || !selectedSituation || !pin) {
            document.getElementById("error-message").innerText = "Zorunlu alanlar boş bırakılamaz!";
            return;
        }

        // 🔹 Tüm eklenen hataları liste olarak gönder
        const defectCatalogIds = addedDefects.map(d => parseInt(d.id));

        const data = {
            tv_seri_no: tvSerial,
            defect_catalog_id: defectCatalogIds,  // ✅ artık liste
            found_by_pin: parseInt(pin),
            status: selectedSituation // ✅ backend ile uyumlu
        };

        console.log("Backend'e gönderilen veri:", data);

        try {
            const response = await fetch("/defect/entry", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                credentials: "include",
                body: JSON.stringify(data)
            });

            const result = await response.json();
            console.log("Backend yanıtı:", result);

            if (response.ok) {
                showSuccessPopup();
            } else {
                document.getElementById("error-message").innerText =
                    result.message || "Bir hata oluştu. Lütfen tekrar deneyin.";
            }

        } catch (err) {
            console.error("İstek hatası:", err);
            document.getElementById("error-message").innerText =
                "Sunucuya bağlanılamadı. Lütfen tekrar deneyin.";
        }
    });

    // 🔹 Başarılı popup
    function showSuccessPopup() {
        const tvSerial = document.getElementById("tv_serial").value.trim();
        const pin = document.getElementById("pin").value.trim();
        const situationText = selectedSituation || "-";
        const defectList = addedDefects.map(d => d.name).join(", ") || "-";

        const popup = document.createElement("div");
        popup.className = "success-popup";
        popup.innerHTML = `
            <div class="popup-content">
                <p><strong>Hata kaydı başarılı!</strong></p>
                <p><strong>TV Seri No:</strong> ${tvSerial}</p>
                <p><strong>Hatalar:</strong> ${defectList}</p>
                <p><strong>Durum:</strong> ${situationText}</p>
                <button id="popupOkBtn">Tamam</button>
            </div>
        `;
        document.body.appendChild(popup);

        document.getElementById("popupOkBtn").addEventListener("click", () => {
            document.body.removeChild(popup);
            resetForm();
        });
    }

    // 🔹 Form sıfırlama
    function resetForm() {
        form.reset();
        addedDefects = [];
        renderDefectTags();
        situationButtons.forEach(b => b.classList.remove("active"));
        selectedSituation = null;
        defectSelect.style.color = "#aaa";
        document.getElementById("error-message").innerText = "";
    }
});

