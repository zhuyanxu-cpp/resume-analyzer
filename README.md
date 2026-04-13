# AI 赋能的智能简历分析系统
北京星使智算科技有限公司（Sidereus AI）Python 后端 / 全栈实习生笔试项目
项目简介
本项目是一个基于 AI 的智能简历分析系统，能够自动解析 PDF 格式的简历，提取关键信息，并利用大语言模型计算简历与岗位需求的匹配度评分。系统采用前后端分离架构，后端基于 FastAPI 构建，前端使用 React 开发，支持 Redis 缓存机制，可部署于阿里云 Serverless 环境。
技术栈
后端技术栈
Web 框架：FastAPI 0.110.0
ASGI 服务器：Uvicorn 0.29.0
PDF 解析：pdfplumber 0.11.0
AI 模型：通义千问 - qwen-turbo
缓存：Redis 5.0.3（支持降级为内存缓存）
部署环境：阿里云函数计算 FC
前端技术栈
前端框架：React 18.2.0
构建工具：Vite 5.2.0
样式框架：Tailwind CSS 3.4.3
HTTP 客户端：Axios 1.6.8
部署环境：GitHub Pages

项目架构
resume-analyzer/
├── backend/                 # 后端代码
│   ├── main.py              # FastAPI主应用，API路由定义
│   ├── pdf_parser.py        # PDF文本解析模块
│   ├── ai_extractor.py      # AI信息提取与匹配度计算
│   ├── cache.py             # Redis缓存模块（支持降级）
│   ├── requirements.txt     # Python依赖包
│   └── .env.example         # 环境变量示例
├── frontend/                # 前端代码
│   ├── src/
│   │   ├── App.jsx          # 主应用组件
│   │   ├── main.jsx         # 应用入口
│   │   └── index.css        # 全局样式
│   ├── index.html           # HTML模板
│   ├── vite.config.js       # Vite配置
│   ├── tailwind.config.js   # Tailwind CSS配置
│   ├── postcss.config.js    # PostCSS配置
│   └── package.json         # Node.js依赖
└── README.md                # 项目说明文档

功能特性
必选功能（已全部实现）
✅ 简历上传与解析：支持上传单个 PDF 格式简历，兼容多页简历，自动提取并清洗文本内容
✅ 关键信息提取：利用 AI 模型提取姓名、电话、邮箱、地址等必选字段
✅ 简历评分与匹配：接收岗位需求描述，计算简历与岗位的匹配度评分
✅ 结果返回：以 JSON 格式结构化返回解析结果、关键信息和匹配度评分
✅ 前端页面：简洁美观的交互页面，支持公开访问
加分功能（已全部实现）
✅ 额外信息提取：支持提取求职意向、期望薪资、工作年限、学历背景、项目经历等加分字段
✅ 缓存机制：实现 Redis 缓存，对已解析和评分的简历进行缓存，避免重复计算
✅ 良好的用户体验：响应式设计，加载状态提示，友好的错误提示
本地运行指南
环境要求
Python 3.10+
Node.js 20.x
Redis（可选，默认使用内存缓存）

后端运行
# 1. 进入后端目录
cd backend

# 2. 创建并激活虚拟环境
python3 -m venv venv
source venv/bin/activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 配置环境变量
cp .env.example .env
# 编辑.env文件，填入通义千问API Key
# DASHSCOPE_API_KEY=your_api_key_here

# 5. 启动后端服务
uvicorn main:app --reload --host 0.0.0.0 --port 8000

后端服务启动后，访问 http://localhost:8000/docs 可查看交互式 API 文档。
前端运行
# 1. 进入前端目录
cd frontend

# 2. 安装依赖
npm install

# 3. 启动开发服务器
npm run dev

前端服务启动后，访问 http://localhost:5173 即可使用系统。
