# 基于Python3.9镜像（适配你的项目依赖）
FROM python:3.9-slim

# 设置容器内的工作目录
WORKDIR /app

# 关键：显式暴露8000端口（解决Back4app的端口检测错误）
EXPOSE 8000

# 复制依赖文件并安装（先复制requirements.txt能利用Docker缓存）
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目所有代码到容器
COPY . .

# 启动命令（和Procfile一致，适配FastAPI）
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]