document.addEventListener("DOMContentLoaded", () => {

    const tableBody = document.querySelector("#defectTable tbody");
    const modal = document.getElementById("defectModal");

    const modalTvModel = document.getElementById("modalTvModel");
    const modalTvSerial = document.getElementById("modalTvSerial");
    const modalDefectName = document.getElementById("modalDefectName");
    const modalDefectDesc = document.getElementById("modalDefectDesc");
    const modalStatus = document.getElementById("modalStatus");
    const modalFoundBy = document.getElementById("modalFoundBy");
    const modalCausedBy = document.getElementById("modalCausedBy");
    const modalReworkBy = document.getElementById("modalReworkBy");

    function getStatusClass(status) {
    if (!status) return "";
    status = status.toUpperCase();
    if (status === "HURDA") return "status-hurda";
    if (status === "REWORK") return "status-rework";
    if (status === "OK") return "status-ok";
    if (status === "CLOSED") return "status-closed";
    return "";
}


    const token = localStorage.getItem("access_token"); // JWT token saklıyorsan

    async function fetchAllDefects() {
        try {
            const res = await fetch("/defect/list", {
                headers: { "Authorization": `Bearer ${token}` }
            });
            const data = await res.json();
            populateTable(data.data || []);
        } catch (err) {
            console.error("Liste alınamadı:", err);
        }
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

    function populateTable(items) {
        tableBody.innerHTML = "";
        items.forEach(item => {
            const row = document.createElement("tr");
            row.innerHTML = `
                <td>${item.id}</td>
                <td>${item.tv_model || '-'}</td>
                <td>${item.tv_seri_no || '-'}</td>
                <td>${item.defect_code || '-'}</td>
                <td>${item.defect_name || '-'}</td>
                <td>${item.defect_description || '-'}</td>
                <td>
                    <span class="status-tag ${getStatusClass(item.status)}">
                        ${item.status || ""}
                    </span>
                </td>
                <td>${formatDateSafe(item.created_at)}</td>
                <td>${item.found_by || '-'}</td>
                <td>${item.rework_by || '-'}</td>
                <td>${item.caused_by || '-'}</td>
            `;
            row.addEventListener("click", () => openModal(item));
            tableBody.appendChild(row);
        });
    }

    function openModal(item) {
        modalTvModel.textContent = item.tv_model || "-";
        modalTvSerial.textContent = item.tv_seri_no || "-";
        modalDefectName.textContent = item.defect_name || "-";
        modalDefectDesc.textContent = item.defect_description || "-";
        modalStatus.textContent = item.status || "-";
        modalFoundBy.textContent = item.found_by || "-";
        modalCausedBy.textContent = item.caused_by || "-";
        modalReworkBy.textContent = item.rework_by || "-";
        modal.style.display = "flex";
    }

    document.getElementById("backButton").addEventListener("click", () => {
    window.history.back(); // bir önceki sayfaya döner
});


    document.getElementById("closeDefectBtn").addEventListener("click", () => {
        modal.style.display = "none";
    });

    window.filterTable = function() {
        const input = document.getElementById("search").value.toLowerCase();
        Array.from(tableBody.getElementsByTagName("tr")).forEach(row => {
            const rowText = row.textContent.toLowerCase();
            row.style.display = rowText.includes(input) ? "" : "none";
        });
    };

    document.getElementById("listAllBtn").addEventListener("click", fetchAllDefects);

    fetchAllDefects();
});
