function searchLogs() {
  const name = document.getElementById("searchName").value.trim();
  const manufacturer = document.getElementById("manufacturerInput").value.trim();
  const start = document.getElementById("startDate").value;
  const end = document.getElementById("endDate").value;

  const url = new URL("http://127.0.0.1:5000/sales/logs");
  if (name) url.searchParams.append("name", name);
  if (manufacturer) url.searchParams.append("manufacturer", manufacturer);
  if (start) url.searchParams.append("start_date", start);
  if (end) url.searchParams.append("end_date", end);

  fetch(url)
    .then(res => res.json())
    .then(data => {
      const tbody = document.querySelector("#salesLogTable tbody");
      tbody.innerHTML = "";

      let totalQty = 0, totalMoney = 0;

      data.forEach(log => {
        const row = document.createElement("tr");
        row.innerHTML = `
          <td>${log.drug_name}</td>
          <td>${log.manufacturer}</td>
          <td>${log.quantity}</td>
          <td>${parseFloat(log.price).toFixed(2)}</td>
          <td>${parseFloat(log.total_price).toFixed(2)}</td>
          <td>${new Date(log.sale_time).toLocaleString()}</td>
        `;
        tbody.appendChild(row);

        totalQty += log.quantity;
        totalMoney += log.total_price;
      });

      document.getElementById("summary").innerText = 
        `💊 ${totalQty} items | 💰 ¥${totalMoney.toFixed(2)}`;
    });
}
