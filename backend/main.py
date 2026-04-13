from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uuid
from pdf_parser import extract_text_from_pdf
from ai_extractor import extract_resume_info, calculate_match_score
from cache import get_cached_result, set_cached_result

app = FastAPI(title="AI简历分析系统")

# 允许跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class JobRequest(BaseModel):
    resume_text: str
    job_description: str

@app.post("/api/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    """上传并解析PDF简历"""
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="只支持PDF格式的简历")
    
    try:
        # 提取PDF文本
        resume_text = await extract_text_from_pdf(file)
        print(f"提取到的PDF文本长度: {len(resume_text)}")
        print(f"PDF文本前500字符:\n{resume_text[:500]}")
        
        # 生成唯一ID用于缓存
        resume_id = str(uuid.uuid5(uuid.NAMESPACE_URL, resume_text[:1000]))
        
        # 检查缓存
        cached_info = get_cached_result(f"info:{resume_id}")
        if cached_info:
            return {"resume_id": resume_id, "resume_info": cached_info, "cached": True, "debug_raw_text": resume_text[:1000]}
        
        # 使用AI提取关键信息
        resume_info = extract_resume_info(resume_text)
        
        # 缓存结果(1小时)
        set_cached_result(f"info:{resume_id}", resume_info, expire=3600)
        
        return {"resume_id": resume_id, "resume_info": resume_info, "cached": False, "debug_raw_text": resume_text[:1000]}
    
    except Exception as e:
        print(f"解析简历异常: {e}")
        raise HTTPException(status_code=500, detail=f"解析简历失败: {str(e)}")

@app.post("/api/match-job")
async def match_job(request: JobRequest):
    """计算简历与岗位的匹配度"""
    try:
        # 生成缓存键
        cache_key = f"match:{hash(request.resume_text[:500] + request.job_description[:500])}"
        
        # 检查缓存
        cached_result = get_cached_result(cache_key)
        if cached_result:
            return {"match_result": cached_result, "cached": True}
        
        # 计算匹配度
        match_result = calculate_match_score(request.resume_text, request.job_description)
        
        # 缓存结果(30分钟)
        set_cached_result(cache_key, match_result, expire=1800)
        
        return {"match_result": match_result, "cached": False}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"计算匹配度失败: {str(e)}")

@app.get("/api/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy", "message": "AI简历分析系统运行正常"}
    
    # ⬇️ 新增以下代码 ⬇️
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9000)
