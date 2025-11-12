document.addEventListener("DOMContentLoaded", () => {

    const sidebarButtons = document.querySelectorAll(".sidebar-btn");
    const tabContents = document.querySelectorAll(".tab-content");

    // İlk tab olarak user tab aktif olsun
    document.getElementById("user-tab").classList.add("active");

    sidebarButtons.forEach(btn => {
        btn.addEventListener("click", () => {
            const tab = btn.getAttribute("data-tab");

            tabContents.forEach(tc => tc.classList.remove("active"));
            document.getElementById(tab + "-tab").classList.add("active");

            if(tab === "tv") loadLineData();
            if(tab === "user") loadUserProfile();
        });
    });

    function loadLineData() {
        fetch("/api/lines")
            .then(res => res.json())
            .then(data => {
                const container = document.getElementById("line-table-container");
                container.innerHTML = "";

                // Table
                const table = document.createElement("table");
                table.innerHTML = `<tr>
                    <th>Line</th>
                    <th>Günlük Hedef</th>
                    <th>Haftalık Hedef</th>
                    <th>Aylık Hedef</th>
                    <th>Hatalı TV</th>
                </tr>`;

                data.forEach(line => {
                    const row = document.createElement("tr");
                    row.innerHTML = `<td>${line.line_name}</td>
                                     <td>${line.daily_target}</td>
                                     <td>${line.weekly_target}</td>
                                     <td>${line.monthly_target}</td>
                                     <td>${line.defective_tv}</td>`;
                    table.appendChild(row);
                });
                container.appendChild(table);

                createLineCharts(data);
            })
            .catch(err => console.error("Line verisi alınamadı:", err));
    }

    function createLineCharts(lines) {
        const chartsContainer = document.getElementById("line-charts");
        chartsContainer.innerHTML = "";

        lines.slice(0, 7).forEach((line, index) => {
            const canvas = document.createElement("canvas");
            canvas.id = `chart-${index}`;
            chartsContainer.appendChild(canvas);

            const defectivePercent = line.defective_tv && line.daily_target
                ? Math.min((line.defective_tv / line.daily_target) * 100, 100)
                : 0;

            new Chart(canvas.getContext("2d"), {
                type: 'doughnut',
                data: {
                    labels: ["Hatalı TV", "Başarılı TV"],
                    datasets: [{
                        data: [defectivePercent, 100 - defectivePercent],
                        backgroundColor: ["#d9534f", "#5cb85c"],
                        borderWidth: 1
                    }]
                },
                options: {
                    plugins: { legend: { display: false } },
                    cutout: '70%',
                    responsive: false,
                }
            });

            const label = document.createElement("div");
            label.textContent = line.line_name;
            label.style.textAlign = "center";
            chartsContainer.appendChild(label);
        });
    }

    function loadUserProfile() {
        fetch("/api/user/profile")
            .then(res => res.json())
            .then(data => {
                const container = document.getElementById("profile-info");
                container.innerHTML = `<p>Ad: ${data.first_name} ${data.last_name}</p>
                                       <p>Kullanıcı Adı: ${data.username}</p>
                                       <p>Pozisyon: ${data.title}</p>`;
            })
            .catch(err => console.error("Profil bilgisi alınamadı:", err));
    }

});
