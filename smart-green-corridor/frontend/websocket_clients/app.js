const titleEl = document.getElementById("app-title");
const subtitleEl = document.getElementById("app-subtitle");
const listEl = document.getElementById("app-list");
const metaEl = document.getElementById("app-meta");

async function loadData() {
  const [configRes, dataRes] = await Promise.all([
    fetch("config.json"),
    fetch("data.json"),
  ]);
  const config = await configRes.json();
  const data = await dataRes.json();
  render(config, data);
}

function render(config, data) {
  titleEl.textContent = config.title;
  subtitleEl.textContent = config.subtitle;
  listEl.innerHTML = "";
  data.items.forEach((item) => {
    const li = document.createElement("li");
    li.textContent = `${item.label} - ${item.value}`;
    listEl.appendChild(li);
  });
  metaEl.textContent = `Updated ${new Date(config.updated_at).toLocaleTimeString()}`;
}

loadData();
