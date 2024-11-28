# Copy Judgment - 英文句子输入正确率检测

## 项目简介

`Copy Judgment` 是一个用于检测英文句子输入正确率的应用，用户上传原始文本后，可以通过输入框逐字输入文本，系统将会计算输入的正确率、输入时间和输入速度（按单词计算）。本项目采用了 Streamlit 作为前端框架，后端使用 Python 进行数据处理，支持用户实时反馈与错误提示。

该项目旨在帮助用户提高英文输入的准确性与速度，并通过实时反馈帮助用户纠正输入错误。

## 项目功能

- **上传文件**：用户可以上传包含原文的 TXT 文件。
- **输入检测**：用户逐字输入文本，系统会逐词对比原文与用户输入，标记正确与错误。
- **输入统计**：计算输入的正确率、输入时间以及输入速度（按单词数计算）。
- **错误反馈**：根据输入正确率给出相应的反馈，如：完全正确、接近正确、偏差较大等。

## 技术栈

- **Python 3.10+**：作为后端开发语言。
- **Streamlit**：用于构建Web应用的框架。
- **Pandas**：数据处理工具。
- **Docker**：项目容器化部署。

## 安装与运行

### 1. 克隆项目

```bash
git clone https://github.com/heike07/copy-judgment.git
cd copy-judgment
```

### 2. 安装依赖

```bash
# 创建虚拟环境（如果没有安装venv，可以先安装）
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/MacOS:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 3.启动应用

```bash
streamlit run app.py
```

### 4.运行 Docker 镜像（可选）

如果你希望使用 Docker 运行该应用，可以按以下步骤操作：

#### 构建镜像

```bash
docker build -t copy-judgment-app .
```

#### 运行容器

```bash
docker run -p 8501:8501 copy-judgment-app
```

访问 `http://localhost:8501` 即可在浏览器中看到应用。

## 使用说明

* 上传包含原文的 TXT 文件。
* 在输入框中逐字输入文本，系统会自动标记输入的正确与错误。
* 输入完成后点击 ​**提交输入**​，系统会计算输入的正确率、时间和速度，并给出反馈。
* 如果需要重新记录，只需刷新页面。

## 项目开发

如果你想对该项目进行修改或贡献，可以按照以下步骤进行开发：

1. Fork 本仓库并克隆到本地。
2. 在 `app.py` 文件中修改功能或界面。
3. 提交 Pull Request

## 联系方式

* ​**GitHub**​: [https://github.com/heike07/copy-judgment](https://github.com/heike07/copy-judgment)
* **Email**: dbj2008@yeah.net











