const path = require("node:path");
const { Jimp, rgbaToInt } = require("jimp");

const assetsDir = path.resolve(__dirname, "../assets");

function makeColor(red, green, blue) {
  return rgbaToInt(red, green, blue, 255);
}

function paintRect(image, left, top, width, height, color) {
  const block = new Jimp({ width, height, color });
  image.composite(block, left, top);
}

async function buildHomeBase() {
  const image = await Jimp.read(path.join(assetsDir, "home-bg.png"));
  const gold = makeColor(206, 178, 122);
  const white = makeColor(255, 255, 255);
  const buttonGold = makeColor(205, 179, 124);

  paintRect(image, 0, 0, 300, 96, gold);
  paintRect(image, 0, 96, 900, 124, gold);
  paintRect(image, 430, 220, 330, 148, white);
  paintRect(image, 40, 430, 1095, 1778, white);
  paintRect(image, 260, 2238, 660, 156, buttonGold);

  await image.write(path.join(assetsDir, "home-base.png"));
}

async function buildDetailBase() {
  const image = await Jimp.read(path.join(assetsDir, "detail-bg.png"));
  const gold = makeColor(206, 178, 122);
  const hero = makeColor(255, 239, 211);
  const white = makeColor(255, 255, 255);

  paintRect(image, 0, 0, 300, 96, gold);
  paintRect(image, 0, 96, 900, 124, gold);
  paintRect(image, 236, 214, 430, 190, hero);
  paintRect(image, 20, 420, 1138, 620, white);

  await image.write(path.join(assetsDir, "detail-base.png"));
}

Promise.all([buildHomeBase(), buildDetailBase()]).catch((error) => {
  console.error(error);
  process.exit(1);
});
