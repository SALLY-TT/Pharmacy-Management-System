document.addEventListener("DOMContentLoaded", () => {
  const username = sessionStorage.getItem("detail_user");
  document.getElementById("summary").innerText = "Detail for: " + username;

  fetch(`http://127.0.0.1:5000/report/seller-detail?username=${username}`)
    .then(res => res.json())
    .then(data => {
      const tbody = document.getElementById("detailBody");
      let total = 0;
      data.records.forEach(row => {
        total += row.total;
        const tr = document.createElement("tr");
        tr.innerHTML = `<td>${row.name}</td><td>${row.quantity}</td><td>${row.price}</td><td>¥${row.total.toFixed(2)}</td><td>${row.timestamp}</td>`;
        tbody.appendChild(tr);
      });
      const summary = document.getElementById("summary");
      summary.innerText += " | Total: ¥" + (data.summary?.total_sales_amount || 0).toFixed(2);
    });
});
