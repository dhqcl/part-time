FROM node:20-alpine AS builder

WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:1.27-alpine

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=builder /app/index.html /usr/share/nginx/html/index.html
COPY --from=builder /app/detail.html /usr/share/nginx/html/detail.html
COPY --from=builder /app/styles.css /usr/share/nginx/html/styles.css
COPY --from=builder /app/app.js /usr/share/nginx/html/app.js
COPY --from=builder /app/content.js /usr/share/nginx/html/content.js
COPY --from=builder /app/assets /usr/share/nginx/html/assets

EXPOSE 80
