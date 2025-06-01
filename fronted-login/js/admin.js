document.addEventListener("DOMContentLoaded", () => {
  const username = sessionStorage.getItem("username");
  const role = sessionStorage.getItem("role");
  const welcome = document.getElementById("welcome");
  const stats = document.getElementById("userStats");
  const userTables = document.getElementById("userTables");
  const msg = document.getElementById("message");

  if (role !== "admin") {
    document.body.innerHTML = "<h2>Access Denied. Admin role required.</h2>";
    return;
  }

  welcome.innerText = "Logged in as: " + username;

  const roles = ["admin", "manager", "seller"];
  const roleColors = {
    admin: { border: "#f8c2ca", background: "#fff5f6", heading: "#d9445c" },
    manager: { border: "#c2e7f8", background: "#f4fcff", heading: "#2b82a0" },
    seller: { border: "#d4f8c2", background: "#f8fff4", heading: "#5c915d" }
  };

  const originalRoles = {};
  let totalCount = 0;
  const roleCounts = { admin: 0, manager: 0, seller: 0 };

  function padId(id) {
    return id.toString().padStart(2, "0");
  }

  function loadUsers() {
    fetch("http://127.0.0.1:5000/users")
      .then(res => res.json())
      .then(users => {
        userTables.innerHTML = "";
        totalCount = users.length;
        roleCounts.admin = roleCounts.manager = roleCounts.seller = 0;
        roles.forEach(r => {
          const container = document.createElement("div");
          const { border, background, heading } = roleColors[r];
          container.style = `
            border: 2px solid ${border};
            background-color: ${background};
            padding: 15px;
            margin-bottom: 20px;
            border-radius: 10px;
          `;

          const title = document.createElement("h3");
          title.innerText = r.toUpperCase() + " Users";
          title.style = `font-size: 24px; font-family: 'Caveat', cursive; color: ${heading}; margin-bottom: 10px;`;
          container.appendChild(title);

          const table = document.createElement("table");
          table.border = 1;
          table.innerHTML = `
            <thead><tr><th>ID</th><th>Username</th><th>Role</th><th>Created At</th><th>Action</th></tr></thead>
            <tbody></tbody>
          `;
          const tbody = table.querySelector("tbody");

          users.filter(u => u.role === r).forEach(user => {
            originalRoles[user.user_id] = user.role;
            roleCounts[r]++;
            const row = document.createElement("tr");
            if (user.username === username) row.style.backgroundColor = "#ffe0e0";
            row.innerHTML = `
              <td>${padId(user.user_id)}</td>
              <td>${user.username}</td>
              <td>
                <span id="role-${user.user_id}">${user.role}</span>
                <select id="select-${user.user_id}" style="display:none;">
                  ${roles.map(opt => `<option value="${opt}" ${opt === user.role ? "selected" : ""}>${opt}</option>`).join("")}
                </select>
              </td>
              <td>${user.created_at}</td>
              <td>
                <button onclick="toggleEdit(${user.user_id})">Edit</button>
                <button onclick="deleteUser(${user.user_id})">Delete</button>
                <button onclick="confirmRoleChange(${user.user_id})" style="display:none;" id="confirm-${user.user_id}">Update</button>
              </td>
            `;
            tbody.appendChild(row);
          });
          container.appendChild(table);

          const addWrapper = document.createElement("div");
          addWrapper.className = "add-user-block";
          addWrapper.innerHTML = `
            <h4 class="add-heading" style="color:${heading};font-family:'Caveat',cursive;">Add New ${r} User</h4>
            <input type="text" placeholder="Username" required id="add-username-${r}">
            <input type="password" placeholder="Password" required id="add-password-${r}">
            <button onclick="addUser('${r}')">Add ${r}</button>
          `;
          container.appendChild(addWrapper);
          userTables.appendChild(container);
        });

        stats.innerText = `👥 Total users: ${totalCount} | Admins: ${roleCounts.admin}, Managers: ${roleCounts.manager}, Sellers: ${roleCounts.seller}`;
        stats.style = "color:#444;margin-bottom:10px;";
      });
  }

  window.addUser = function (r) {
    const username = document.getElementById(`add-username-${r}`).value;
    const password = document.getElementById(`add-password-${r}`).value;
    fetch("http://127.0.0.1:5000/users", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password, role: r })
    })
      .then(res => res.json())
      .then(result => {
        msg.innerText = result.message;
        loadUsers();
      });
  };

  window.toggleEdit = function (user_id) {
    document.getElementById(`role-${user_id}`).style.display = "none";
    document.getElementById(`select-${user_id}`).style.display = "inline";
    document.getElementById(`confirm-${user_id}`).style.display = "inline";
  };

  window.confirmRoleChange = function (user_id) {
    const select = document.getElementById(`select-${user_id}`);
    const newRole = select.value;
    const oldRole = originalRoles[user_id];

    const confirmChange = confirm(`Confirm changing role to "${newRole}"?`);
    if (!confirmChange) {
      select.value = oldRole;
      select.style.display = "none";
      document.getElementById(`role-${user_id}`).style.display = "inline";
      document.getElementById(`confirm-${user_id}`).style.display = "none";
      return;
    }

    fetch(`http://127.0.0.1:5000/users/${user_id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ role: newRole })
    })
      .then(res => res.json())
      .then(result => {
        msg.innerText = result.message;
        loadUsers();
      });
  };

  window.deleteUser = function (user_id) {
    if (!confirm("Are you sure you want to delete this user?")) return;
    fetch(`http://127.0.0.1:5000/users/${user_id}`, {
      method: "DELETE"
    })
      .then(res => res.json())
      .then(result => {
        msg.innerText = result.message;
        loadUsers();
      });
  };

  loadUsers();
});
