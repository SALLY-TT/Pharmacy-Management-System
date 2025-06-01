
let drugList = [];
let cart = [];
let currentPage = 1;
const perPage = 8;

// 拉取药品数据（从数据库）
function loadDrugsFromServer() {
  fetch("http://127.0.0.1:5000/drugs?page=1&limit=1000")
    .then(res => res.json())
    .then(data => {
      drugList = data.drugs.map(d => ({
        id: d.drug_id,
        name: d.name,
        manufacturer: d.manufacturer,
        price: d.price,
        stock: d.stock,
        code: d.code
      }));
      renderDrugs();
    });
}

// 渲染药品信息表格（含分页与低库存提示）
function renderDrugs() {
  const nameKeyword = document.getElementById("searchNameInput").value.toLowerCase();
  const manuKeyword = document.getElementById("searchManufacturerInput").value.toLowerCase();
  const tbody = document.getElementById("drugTable");
  tbody.innerHTML = "";


  const filtered = drugList
  .filter(d =>
    d.name.toLowerCase().includes(nameKeyword) &&
    d.manufacturer.toLowerCase().includes(manuKeyword)
  );

  const sortBy = document.getElementById("sortBy").value;
  if (sortBy === "price-asc") filtered.sort((a, b) => a.price - b.price);
  if (sortBy === "price-desc") filtered.sort((a, b) => b.price - a.price);
  if (sortBy === "stock-asc") filtered.sort((a, b) => a.stock - b.stock);
  if (sortBy === "stock-desc") filtered.sort((a, b) => b.stock - a.stock);

  const start = (currentPage - 1) * perPage;
  const pageData = filtered.slice(start, start + perPage);

  pageData.forEach(drug => {
    const row = document.createElement("tr");
    const stockDisplay = drug.stock <= 5 ? `<span style='color:red;'>${drug.stock} ⚠ Low stock</span>` : drug.stock;
    row.innerHTML = `
      <td>${drug.id}</td>
      <td>${drug.name}</td>
      <td>${drug.manufacturer}</td>
      <td>$${drug.price}</td>
      <td>${stockDisplay}</td>
      <td>${drug.code}</td>
      <td>
        <input type="number" min="1" value="1" id="qty-${drug.id}" style="width:60px;">
        <button onclick="addToCart(${drug.id}, '${drug.name}', ${drug.price})">Add</button>
      </td>
    `;
    tbody.appendChild(row);
  });

  const totalPages = Math.ceil(filtered.length / perPage);
  const pagination = document.getElementById("pagination");
  pagination.innerHTML = "";
  for (let i = 1; i <= totalPages; i++) {
    const btn = document.createElement("button");
    btn.innerText = i;
    btn.disabled = (i === currentPage);
    btn.onclick = () => { currentPage = i; renderDrugs(); };
    pagination.appendChild(btn);
  }
}

// 加入购物车：若已有则合并数量
function addToCart(drug_id, name, price) {
  const qtyInput = document.getElementById(`qty-${drug_id}`);  // 定义 qtyInput
  const qty = parseInt(qtyInput.value);
  if (!qty || qty <= 0) return;

  const drug = drugList.find(d => d.id === drug_id);
  if (!drug) {
    alert("Drug not found.");
    return;
  }

  const existing = cart.find(i => i.drug_id === drug_id && i.price === price);
  const totalQuantity = existing ? existing.quantity + qty : qty;

  if (totalQuantity > drug.stock) {
    alert(`库存不足：最多可购买 ${drug.stock - (existing ? existing.quantity : 0)} 件`);
    qtyInput.value = 1;  // 重置为 1
    return;
  }

  if (existing) {
    existing.quantity += qty;
  } else {
    cart.push({ drug_id, name, price, quantity: qty });
  }

  renderCart();
}

// 渲染购物车表格
function renderCart() {
  const tbody = document.querySelector("#cartTable tbody");
  tbody.innerHTML = "";
  cart.forEach((item, index) => {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${item.name}</td>
      <td>${item.quantity}</td>
      <td>
        <button onclick="adjustQuantity(${index}, 1)">＋</button>
        <button onclick="adjustQuantity(${index}, -1)">－</button>
      </td>
      <td><button onclick="removeFromCart(${index})">❌</button></td>
    `;
    tbody.appendChild(row);
  });
  
}

// 调整购物车数量，若为0则删除
function adjustQuantity(index, delta) {
  cart[index].quantity += delta;
  if (cart[index].quantity <= 0) {
    cart.splice(index, 1);
  }
  renderCart();
}

function removeFromCart(index) {
  cart.splice(index, 1);
  renderCart();
}

// 提交订单，逐个发送 POST /sales
function submitOrder() {
  if (cart.length === 0) {
    alert("Cart is empty.");
    return;
  }
  const username = sessionStorage.getItem("username");
  if (!username) {
    alert("No seller username found.");
    return;
  }

  // 构造一个数组，每项都包含 seller_username + drug_id + quantity
  const payload = cart.map(item => ({
    seller_username: username,
    drug_id: item.drug_id,
    quantity: item.quantity
  }));

  // 提交整个数组
  fetch("http://127.0.0.1:5000/sales", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  })
    .then(res => res.json())
    .then(result => {
      if (result.errors && result.errors.length > 0) {
        alert("Some sales failed:\n" + result.errors.join("\n"));
      } else {
        alert("All sales submitted successfully.");
        cart = [];
        renderCart();
        loadDrugsFromServer(); // 更新库存
      }
    })
    .catch(error => {
      alert("Request failed:\n" + error);
    });
}
//一键清空购物车
function clearCart() {
  if (cart.length === 0) {
    alert("Cart is already empty.");
    return;
  }
  if (confirm("Are you sure you want to clear the cart?")) {
    cart = [];
    renderCart();
  }
}

document.getElementById("searchNameInput").addEventListener("input", renderDrugs);
document.getElementById("searchManufacturerInput").addEventListener("input", renderDrugs);
document.getElementById("sortBy").addEventListener("change", renderDrugs);
loadDrugsFromServer();
