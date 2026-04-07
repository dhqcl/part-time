(function attachPageContent(globalScope) {
  const pageContent = {
    common: {
      headerBack: "返回",
      headerClose: "关闭",
      headerTitle: "文明养犬一件事"
    },
    home: {
      petCodeLabel: "宠物码",
      petName: "八喜",
      vaccineLabel: "最后免疫日期：",
      vaccineDate: "2025-12-27",
      registerLabel: "最后登记日期：",
      registerDate: "2026-02-28",
      alertTitle: "《免疫证明》《养犬登记证》有效",
      alertDescription:
        "该宠物《免疫证明》、《养犬登记证》均在有效期！",
      detailButton: "查看详情",
      qrValue: "文明养犬电子证件|八喜|9417000270|柴犬|黑色"
    },
    detail: {
      petName: "八喜",
      genderSymbol: "♀",
      summaryLeft: "柴犬",
      summaryRight: "黑色",
      fields: [
        ["免疫证号", "9417000270"],
        ["电子芯片号", "1560*******266"],
        ["犬只名称", "八喜"],
        ["犬品种", "柴犬"],
        ["犬毛色", "黑色"],
        ["最后免疫日期", "2025-12-27"],
        ["最后登记日期", "2026-02-28"]
      ]
    }
  };

  globalScope.pageContent = pageContent;

  if (typeof module !== "undefined" && module.exports) {
    module.exports = { pageContent };
  }
})(typeof window !== "undefined" ? window : globalThis);
