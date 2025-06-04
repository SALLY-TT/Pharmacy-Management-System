document.addEventListener("DOMContentLoaded", () => {
  fetch("http://127.0.0.1:5000/operation/logs")
    .then(res => res.json())
    .then(logs => {
      const tbody = document.querySelector("#operationLogTable tbody");
      tbody.innerHTML = "";

      logs.forEach(log => {
        const row = document.createElement("tr");
        row.innerHTML = `
          <td>${log.username}</td>
          <td>${log.operation_type}</td>
          <td>${log.drug_id}</td>
          <td>${log.drug_name}</td>
          <td>${log.description}</td>
          <td>${new Date(log.time).toLocaleString()}</td>
        `;
        tbody.appendChild(row);
      });
    })
    .catch(err => {
      console.error("Failed to load logs:", err);
    });
});
