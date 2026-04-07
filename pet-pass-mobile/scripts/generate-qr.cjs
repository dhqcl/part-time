const path = require("node:path");
const QRCode = require("qrcode");
const { pageContent } = require("../content.js");

const outputPath = path.resolve(__dirname, "../assets/qr-code.svg");

QRCode.toFile(outputPath, pageContent.home.qrValue, {
  errorCorrectionLevel: "M",
  margin: 0,
  type: "svg",
  width: 564,
  color: {
    dark: "#2ea84d",
    light: "#ffffff"
  }
}).catch((error) => {
  console.error(error);
  process.exit(1);
});
