document.addEventListener("DOMContentLoaded", () => {
  const username = sessionStorage.getItem("username");
  if (!username) {
    document.body.innerHTML = "<h2>请先登录</h2>";
    return;
  }

  console.log("当前用户名:", username);
  const reportTable = document.getElementById("reportTable");
  const totalDisplay = document.getElementById("total");

  fetch(`http://127.0.0.1:5000/sales/report?username=${username}`)
    .then(res => res.json())
    .then(data => {
      if (!data.sales || data.sales.length === 0) {
        totalDisplay.innerText = "暂无销售记录。";
        return;
      }

      const rows = data.sales.map(sale => `
        <tr>
          <td>${sale.drug_id}</td>
          <td>${sale.drug_name}</td>
          <td>${sale.drug_manufacturer}</td>
          <td>${sale.quantity}</td>
          <td>${sale.price}</td>
          <td>¥${sale.total_price}</td>
          <td>${sale.sale_time}</td>
        </tr>
      `).join("");
      reportTable.innerHTML = rows;
      totalDisplay.innerText = `总销售额：￥${data.total_sales}`;
    })
    .catch(err => {
      console.error("加载销售报告失败:", err);
      totalDisplay.innerText = "加载失败，请检查网络或服务器。";
    });
});
