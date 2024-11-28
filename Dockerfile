# 使用官方的 Python 镜像作为基础镜像
FROM python:3.10

# 设置工作目录
WORKDIR /app

# 复制当前目录下的所有文件到容器中的 /app 目录
COPY . /app

# 安装程序所需的 Python 库
RUN pip install --no-cache-dir -r requirements.txt

# 开放 8501 端口（Streamlit 默认端口）
EXPOSE 8501

# 设置容器启动时的命令，运行 Streamlit 应用
CMD ["streamlit", "run", "app.py"]
