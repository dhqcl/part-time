const pageContent = window.pageContent || {};
const fullTimeNodes = document.querySelectorAll("[data-full-time]");
const statusTimeNodes = document.querySelectorAll("[data-status-time]");
const textNodes = document.querySelectorAll("[data-field]");
const detailFieldsNode = document.querySelector("[data-detail-fields]");

const fullFormatter = new Intl.DateTimeFormat("zh-CN", {
  timeZone: "Asia/Shanghai",
  year: "numeric",
  month: "2-digit",
  day: "2-digit",
  hour: "2-digit",
  minute: "2-digit",
  second: "2-digit",
  hour12: false
});

const statusFormatter = new Intl.DateTimeFormat("zh-CN", {
  timeZone: "Asia/Shanghai",
  hour: "2-digit",
  minute: "2-digit",
  hour12: false
});

function toPartsMap(parts) {
  return parts.reduce((accumulator, part) => {
    if (part.type !== "literal") {
      accumulator[part.type] = part.value;
    }

    return accumulator;
  }, {});
}

function getFullTimeText(date) {
  const parts = toPartsMap(fullFormatter.formatToParts(date));
  return `${parts.year}-${parts.month}-${parts.day} ${parts.hour}:${parts.minute}:${parts.second}`;
}

function getValueByPath(source, path) {
  return path.split(".").reduce((value, key) => value?.[key], source);
}

function renderStaticCopy() {
  textNodes.forEach((node) => {
    const fieldPath = node.dataset.field;
    const value = getValueByPath(pageContent, fieldPath);

    if (typeof value === "string") {
      node.textContent = value;
    }
  });

  if (detailFieldsNode) {
    const fragment = document.createDocumentFragment();

    (pageContent.detail?.fields || []).forEach(([label, value]) => {
      const row = document.createElement("div");
      row.className = "detail-field-row";

      const labelNode = document.createElement("span");
      labelNode.className = "detail-field-label";
      labelNode.textContent = label;

      const valueNode = document.createElement("span");
      valueNode.className = "detail-field-value";
      valueNode.textContent = value;

      row.append(labelNode, valueNode);
      fragment.append(row);
    });

    detailFieldsNode.replaceChildren(fragment);
  }
}

function updateTimes() {
  const now = new Date();
  const fullTime = getFullTimeText(now);
  const statusTime = statusFormatter.format(now);

  fullTimeNodes.forEach((node) => {
    node.textContent = fullTime;
  });

  statusTimeNodes.forEach((node) => {
    node.textContent = statusTime;
  });
}

renderStaticCopy();
updateTimes();
setInterval(updateTimes, 1000);
