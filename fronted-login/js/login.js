document.getElementById("loginForm").addEventListener("submit", function(e) {
  e.preventDefault();
  const username = document.getElementById("username").value.trim();
  const password = document.getElementById("password").value;

  fetch("http://127.0.0.1:5000/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password })
  })
    .then(res => res.json())
    .then(data => {
      if (data.message=="Login successful") {
        sessionStorage.setItem("username", data.username);
        sessionStorage.setItem("role", data.role);

        // 根据用户角色跳转不同页面
        if (data.role === "admin") {
          window.location.href = "admin.html";
        } else if (data.role === "manager") {
          window.location.href = "manager_dashboard.html";
        } 
        else {
          // 默认跳转 fallback
          window.location.href = "main.html";
        }

      } else {
        document.getElementById("message").innerText = data.message;
      }
    });
});
