# Erstelle das Build mit Node.js
FROM node:18 AS builder
WORKDIR /app

# Abhängigkeiten installieren
COPY package.json package-lock.json ./
RUN npm install

# Kopiere den Code und baue Tailwind CSS
COPY . .
RUN npm run build

# Verwende Nginx für die Bereitstellung
FROM nginx:alpine

COPY nginx.conf /etc/nginx/nginx.conf

COPY --from=builder /app/dist /usr/share/nginx/html
