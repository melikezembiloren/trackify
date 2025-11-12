function handleLogin(isLine) {
    var username = document.getElementById("username").value.trim();
    var password = document.getElementById("password").value.trim();
    var errorMsg = document.getElementById("error-message");

    errorMsg.textContent = "";

    if (!username || !password) {
        errorMsg.textContent = "Lütfen tüm alanları doldurun.";
        return;
    }

    var endpoint = isLine ? "/login/line" : "/login/user";
    var body = isLine 
        ? JSON.stringify({ linename: username, password: password })
        : JSON.stringify({ username: username, password: password });

    // XMLHttpRequest ile desteklenmeyen fetch yerine
    var xhr = new XMLHttpRequest();
    xhr.open("POST", endpoint, true);
    xhr.setRequestHeader("Content-Type", "application/json");

    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
            if (xhr.status >= 200 && xhr.status < 300) {
                var data;
                try { data = JSON.parse(xhr.responseText); } 
                catch(e) { data = {}; }

                if (isLine) {
                    window.location.href = "/process/selection";
                } else {
                    window.location.href = "/dashboard";
                }
            } else {
                try { 
                    var data = JSON.parse(xhr.responseText);
                    errorMsg.textContent = data.message || "Kullanıcı adı veya şifre hatalı.";
                } catch(e) {
                    errorMsg.textContent = "Kullanıcı adı veya şifre hatalı.";
                }
            }
        }
    };

    xhr.onerror = function() {
        errorMsg.textContent = "Sunucuya bağlanılamadı. Lütfen tekrar deneyin.";
    };

    xhr.send(body);
}

// Event listener
document.getElementById("userLoginBtn").onclick = function() {
    handleLogin(false);
};
document.getElementById("lineLoginBtn").onclick = function() {
    handleLogin(true);
};
