# Pet Pass Mobile

这是一个按截图还原的移动端静态页面，首页展示宠物码，点击 `查看详情` 会跳转到详情页。

## 修改文案

页面里的可见文字统一放在 [content.js](/Users/mini/Documents/codex/part-time/pet-pass-mobile/content.js)：

- 首页标题、姓名、日期、提示文案、按钮文案
- 详情页姓名、性别、摘要、字段列表
- 二维码内容

修改完后重新执行：

```bash
npm run build
```

## 本地生成二维码

```bash
npm install
npm run build
```

## 本地预览 HTML

可以直接打开这两个文件预览：

- [index.html](/Users/mini/Documents/codex/part-time/pet-pass-mobile/index.html)
- [detail.html](/Users/mini/Documents/codex/part-time/pet-pass-mobile/detail.html)

如果浏览器对本地模块加载有限制，建议在项目目录执行：

```bash
npm run preview
```

然后访问：

- [http://127.0.0.1:7180/](http://127.0.0.1:7180/)

## Docker 启动

```bash
docker compose up -d --build
```

启动后访问：

- `http://服务器IP:718/`

说明：

- 你提到的 `0718` 在浏览器地址里实际写法通常是 `718`
- 如果要在 iPhone 上从公网访问，请确保云服务器安全组和防火墙放行 `718` 端口

## 云服务器一键部署

在服务器项目目录执行：

```bash
chmod +x deploy.sh
./deploy.sh
```

如果你想显式指定端口，也可以这样：

```bash
./deploy.sh 718
```
