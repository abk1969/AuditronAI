FROM node:18-alpine

WORKDIR /app

# Installation des dépendances
COPY package.json package-lock.json ./
RUN npm install

# Copie du code source
COPY . .

# Construction de l'application
RUN npm run build

# Installation de serve pour servir l'application
RUN npm install -g serve

# Exposition du port
EXPOSE 3000

# Commande de démarrage
CMD ["serve", "-s", "build", "-l", "3000"] 