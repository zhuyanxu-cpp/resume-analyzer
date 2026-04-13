# AI 赋能的智能简历分析系统

> 星使智算（Sidereus AI）Python 后端/全栈实习生笔试题

## 📌 项目简介
本项目是一个基于 AI 大模型的智能简历分析系统，能够自动解析 PDF 格式简历，提取关键信息，并与岗位需求进行匹配度计算，帮助招聘者快速筛选候选人。

## 🚀 技术栈
### 后端
- **开发语言**：Python 3.10
- **Web 框架**：FastAPI（高性能异步 Web 框架）
- **AI 模型**：通义千问（DashScope API）
- **缓存**：Redis（避免重复计算，提升性能）
- **PDF 解析**：pdfplumber（精准提取 PDF 文本）
- **部署环境**：阿里云函数计算 FC（Serverless 架构，按需启动，24 小时在线）

### 前端
- **开发语言**：JavaScript
- **框架**：React 18
- **构建工具**：Vite
- **HTTP 客户端**：Axios
- **部署环境**：GitHub Pages（公网可访问）

## 📂 项目结构
resume-analyzer/
├── backend/ # 后端代码
│ ├── main.py # FastAPI 主入口
│ ├── pdf_parser.py # PDF 文本解析
│ ├── ai_extractor.py # AI 关键信息提取
│ ├── cache.py # Redis 缓存
│ ├── requirements.txt # 依赖列表
│ └── .env # 环境变量（API Key）
├── frontend/ # 前端代码
│ ├── src/
│ │ └── App.jsx # 主页面
│ ├── vite.config.js # Vite 配置
│ └── package.json # 前端依赖
└── README.md # 项目文档


## ✨ 核心功能
### 1. 简历上传与解析
- 支持上传单个 PDF 格式简历
- 兼容多页简历，精准提取文本
- 自动清洗冗余字符，合理分段

### 2. AI 关键信息提取
利用通义千问大模型提取：
- **基本信息**：姓名、电话、邮箱、地址
- **求职信息**：求职意向、期望薪资
- **背景信息**：工作年限、学历背景、项目经历

### 3. 简历评分与匹配
- 接收岗位需求描述
- 自动提取岗位关键词
- 计算简历与岗位的匹配度评分
- 技能匹配率、工作经验相关性综合评估

### 4. 结果返回与缓存
- JSON 格式结构化返回
- Redis 缓存已解析简历，避免重复 AI 调用
- 缓存有效期：简历信息 1 小时，匹配结果 30 分钟

## 🌐 线上演示
### 前端地址
`https://你的GitHub用户名.github.io/resume-analyzer/`

### 后端 API 地址
`https://resume-yzer-new-crkmwwlaab.cn-hangzhou.fcapp.run`

### 健康检查接口
`https://resume-yzer-new-crkmwwlaab.cn-hangzhou.fcapp.run/api/health`

## 🚀 部署方式
### 后端部署（阿里云 FC）
1.  进入阿里云函数计算 FC 控制台
2.  创建 Web 函数，选择「自定义运行时 Python 3.10 Debian 11」
3.  上传代码包 `code.zip`
4.  配置启动命令：`["/bin/bash", "-c", "pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple && python main.py"]`
5.  配置监听端口：9000
6.  配置环境变量：`DASHSCOPE_API_KEY`
7.  创建 HTTP 触发器，认证方式「无需认证」，允许方法 `GET/POST/OPTIONS`
8.  部署完成

### 前端部署（GitHub Pages）
1.  修改 `vite.config.js`，添加 `base: '/resume-analyzer/'`
2.  安装 `gh-pages`：`npm install --save-dev gh-pages`
3.  修改 `package.json`，添加 `predeploy` 和 `deploy` 脚本
4.  执行 `npm run deploy`
5.  在 GitHub Settings → Pages 中获取线上地址

## 📝 使用说明
1.  打开前端页面
2.  上传 PDF 格式简历
3.  点击「解析简历」，等待 AI 提取信息
4.  输入岗位需求描述
5.  点击「计算匹配度」，查看匹配结果

## 🎯 技术亮点
1.  **Serverless 架构**：阿里云 FC 按需启动，无需维护服务器，24 小时在线
2.  **AI 大模型集成**：通义千问精准提取简历信息，匹配度计算更智能
3.  **Redis 缓存**：避免重复 AI 调用，降低成本，提升响应速度
4.  **前后端分离**：React + FastAPI，架构清晰，易于维护
5.  **跨域支持**：CORS 中间件，前端可直接调用后端 API
6.  **工程化实践**：Git 提交规范，专业 README 文档，错误处理完善

## 📄 许可证
MIT License
