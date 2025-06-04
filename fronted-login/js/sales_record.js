let currentPage = 1;        // 当前页码
const pageSize = 8;         // 每页显示条数
let totalPages = 1;         // 总页数，后端返回
let currentQuery = {};      // 当前查询参数，方便翻页时复用

document.addEventListener("DOMContentLoaded", () => {
  const username = sessionStorage.getItem("username");
  const role = sessionStorage.getItem("role");

  // 权限校验
  if (!username || role !== "manager") {
    document.body.innerHTML = "<h2 style='color: #333; padding: 2rem;'>🛑 Access Denied. Manager role required.</h2>";
    return;
  }

  // 显示用户名
  document.getElementById("username").innerText = username;

  // 加载销售记录
  searchLogs();
});

// 主查询函数：调用后端接口加载销售记录
function searchLogs(page = 1) {
  const name = document.getElementById("searchName").value.trim();
  const manufacturer = document.getElementById("manufacturerInput").value.trim();
  const start = document.getElementById("startDate").value;
  const end = document.getElementById("endDate").value;

  // 记录当前查询条件
  currentQuery = { name, manufacturer, start, end };
  currentPage = page;

  const url = new URL("http://127.0.0.1:5000/sales/logs");
  url.searchParams.append("page", currentPage);
  url.searchParams.append("limit", pageSize);
  if (name) url.searchParams.append("name", name);
  if (manufacturer) url.searchParams.append("manufacturer", manufacturer);
  if (start) url.searchParams.append("start_date", start);
  if (end) url.searchParams.append("end_date", end);

  fetch(url)
    .then(res => res.json())
    .then(data => {
      renderLogs(data.logs);
      renderPagination(data.total_pages);
      renderSummary(data.stats);
    })
    .catch(err => console.error("Failed to fetch sales logs:", err));
}

// 渲染表格内容
function renderLogs(logs) {
  const tbody = document.querySelector("#salesLogTable tbody");
  tbody.innerHTML = "";

  logs.forEach(log => {
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
  });
}

// 渲染分页按钮
function renderPagination(pages) {
  totalPages = pages;
  const pagination = document.getElementById("pagination");
  pagination.innerHTML = "";

  for (let i = 1; i <= totalPages; i++) {
    const btn = document.createElement("button");
    btn.textContent = i;
    btn.disabled = i === currentPage;
    btn.onclick = () => searchLogs(i);
    pagination.appendChild(btn);
  }
}

// 渲染总计数据
function renderSummary(stats) {
  const totalQty = stats.total_items || 0;
  const totalMoney = stats.total_amount || 0;
  document.getElementById("summary").innerText =
    `💊 ${totalQty} items | 💰 ¥${parseFloat(totalMoney).toFixed(2)}`;
}

// 页面加载后立即加载全部数据（默认第一页）
document.addEventListener("DOMContentLoaded", () => searchLogs());

// Enter 键快捷搜索
document.addEventListener("keydown", (e) => {
  if (e.key === "Enter") {
    searchLogs(); // 默认为第一页
  }
});
