FROM mcr.microsoft.com/playwright:v1.58.2-jammy

WORKDIR /app

RUN apt-get update && apt-get install -y python3 python3-pip

COPY package*.json ./
COPY requirements.txt ./

RUN npm install && pip3 install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["npx", "playwright", "test"]