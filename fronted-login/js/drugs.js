document.addEventListener("DOMContentLoaded", () => {
  // 获取当前用户的用户名和角色
  const username = sessionStorage.getItem("username");
  const role = sessionStorage.getItem("role");
  
document.addEventListener("keydown", function(e) {
  if (e.key === "Enter") {
    searchDrugs();
  }
});

  // 获取表格、消息区域和分页容器的引用
  const tableBody = document.querySelector("#drugTable tbody");
  const msg = document.getElementById("message");
  const pagination = document.getElementById("pagination");

  // 如果不是管理员角色，拒绝访问
  if (role !== "manager") {
    document.body.innerHTML = "<h2>Access Denied. Manager role required.</h2>";
    return;
  }

  // 显示欢迎信息
  document.getElementById("welcome").innerText = "Logged in as: " + username;

  // 定义全局状态变量：当前页、搜索关键字、厂家筛选、排序字段
  let currentPage = 1;
  let currentName = "";
  let currentManufacturer = "";
  let currentSortBy = "";

  // 加载药品信息并渲染表格
  function loadDrugs(page = currentPage, name = currentName, manufacturer = currentManufacturer, sortBy = currentSortBy) {
    // 更新当前状态
    currentPage = page;
    currentName = name;
    currentManufacturer = manufacturer;
    currentSortBy = sortBy;

    // 构造请求 URL，附加查询参数
    const url = new URL("http://127.0.0.1:5000/drugs");
    url.searchParams.append("page", page);
    url.searchParams.append("limit", 8);
    if (name) url.searchParams.append("name", name);
    if (manufacturer) url.searchParams.append("manufacturer", manufacturer);
    if (sortBy) url.searchParams.append("sort", sortBy);

    // 发送请求获取药品数据
    fetch(url)
      .then(res => res.json())
      .then(data => {
        const drugs = data.drugs;
        const totalPages = data.total_pages;

        // 清空旧数据
        tableBody.innerHTML = "";

        // 遍历药品数据生成表格行
        drugs.forEach(drug => {
          const row = document.createElement("tr");
          row.innerHTML = `
            <td>${drug.drug_id}</td>
            <td id="name-${drug.drug_id}">${drug.name}</td>
            <td id="manufacturer-${drug.drug_id}">${drug.manufacturer}</td>
            <td><input type="number" id="price-${drug.drug_id}" value="${drug.price}" step="0.01"></td>
            <td><input type="number" id="stock-${drug.drug_id}" value="${drug.stock}" min="0"></td>
            <td id="code-${drug.drug_id}">${drug.code}</td>
            <td>${drug.total_sold || 0}</td>
            <td>${drug.sold_since_restock || 0}</td>
            <td>${drug.last_updated || "-"}</td>
            <td>${drug.last_updated_by || "-"}</td> 
            <td>
              <button class="btn-green" onclick="updateDrug(${drug.drug_id})">Update</button>
              <button class="btn-blue" onclick="deleteDrug(${drug.drug_id})">Delete</button>
            </td>
          `;
          tableBody.appendChild(row);
        });

        // 渲染分页按钮
        renderPagination(totalPages, page);
      });
  }

  // 渲染分页按钮
  function renderPagination(totalPages, activePage) {
    pagination.innerHTML = "";
    for (let i = 1; i <= totalPages; i++) {
      const btn = document.createElement("button");
      btn.innerText = i;
      btn.className = "btn-green";
      if (i === activePage) btn.disabled = true;
      btn.onclick = () => {
        loadDrugs(i); // 点击页码按钮后加载对应页
      };
      pagination.appendChild(btn);
    }
  }

  // 搜索药品（全局函数，可被按钮调用）
  window.searchDrugs = function () {
    const name = document.getElementById("searchNameInput").value.trim().toLowerCase();
    const manufacturer = document.getElementById("searchManufacturerInput").value.trim().toLowerCase();
    const sortBy = document.getElementById("sortBy").value;

    // 重置为第一页，更新查询状态
    currentPage = 1;
    currentName = name;
    currentManufacturer = manufacturer;
    currentSortBy = sortBy;
  
    loadDrugs(currentPage, name, manufacturer, sortBy);
    
  };

  // 删除药品（全局函数）
  window.deleteDrug = function(drug_id) {
    fetch(`http://127.0.0.1:5000/drugs/${drug_id}`, {
      method: "DELETE",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username })
    })
    .then(res => res.json())
    .then(result => {
      alert(result.message);
      loadDrugs(); // 重新加载当前页面数据
    });
  };

  // 更新药品信息（全局函数）
  window.updateDrug = function(drug_id) {
    const newPrice = parseFloat(document.getElementById(`price-${drug_id}`).value);
    const newStock = parseInt(document.getElementById(`stock-${drug_id}`).value);
    const name = document.getElementById(`name-${drug_id}`).innerText;
    const manufacturer = document.getElementById(`manufacturer-${drug_id}`).innerText;
    const code = document.getElementById(`code-${drug_id}`).innerText;

    fetch(`http://127.0.0.1:5000/drugs/${drug_id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        username,
        name,
        manufacturer,
        price: newPrice,
        stock: newStock,
        code
      })
    })
    .then(res => res.json())
    .then(result => {
      alert(result.message);
      loadDrugs(); // 重新加载当前页面数据
    });
  };

  // 添加药品的表单提交事件处理
  document.getElementById("addDrugForm").addEventListener("submit", function(e) {
    e.preventDefault();

    // 构造要添加的药品对象
    const drug = {
      username,
      name: document.getElementById("name").value,
      manufacturer: document.getElementById("manufacturer").value,
      price: parseFloat(document.getElementById("price").value),
      stock: parseInt(document.getElementById("stock").value),
      code: document.getElementById("code").value
    };

    fetch("http://127.0.0.1:5000/drugs", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(drug)
    })
    .then(res => res.json())
    .then(result => {
      msg.innerText = result.message;
      loadDrugs(); // 添加成功后刷新表格
      this.reset(); // 清空表单
    });
  });

  // 页面加载完毕后首次加载药品数据
  loadDrugs();
});
