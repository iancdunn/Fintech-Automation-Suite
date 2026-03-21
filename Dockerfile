FROM mcr.microsoft.com/playwright:v1.58.2-jammy

WORKDIR /app

RUN apt-get update && apt-get install -y python3 python3-pip

COPY package*.json ./
RUN npm install

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["npx", "playwright", "test"]
