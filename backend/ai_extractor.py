import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()
DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")

def call_qwen(prompt: str) -> str:
    """调用通义千问API"""
    url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
    headers = {
        "Authorization": f"Bearer {DASHSCOPE_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "qwen-turbo",  # 换成更强大的模型
        "input": {
            "messages": [
                {"role": "user", "content": prompt}
            ]
        },
        "parameters": {
            "result_format": "message",
            "temperature": 0.1,
            "max_tokens": 1000
        }
    }
    
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()["output"]["choices"][0]["message"]["content"]

def extract_resume_info(resume_text: str) -> dict:
    """从简历文本中提取关键信息"""
    prompt = f"""
    你是一个专业的简历信息提取助手。请严格按照以下要求从简历文本中提取信息：
    
    1. 必须提取的字段：
       - name: 姓名（字符串）
       - phone: 电话号码（11位数字）
       - email: 电子邮箱地址
       - address: 籍贯或现居地
    
    2. 可选提取的字段：
       - job_intention: 应聘岗位
       - expected_salary: 期望薪资
       - work_years: 工作年限（应届生写"应届"）
       - education: 最高学历（如"硕士研究生"）
       - projects: 项目经历列表（数组，每个元素是一个项目名称）
    
    3. 严格遵守以下规则：
       - 如果某个字段没有找到，必须设置为 null
       - 只返回标准的JSON格式，不要任何其他文字、解释或markdown
       - 不要添加任何不在上述列表中的字段
       - 确保JSON语法完全正确，没有多余的逗号
    
    简历文本：
    {resume_text[:4000]}
    
    只返回JSON，不要任何其他内容！
    """
    
    try:
        result = call_qwen(prompt)
        print(f"\n========== AI返回的原始内容 ==========")
        print(result)
        print(f"=======================================\n")

        # 更健壮的JSON解析
        result = result.strip()
        # 移除可能的markdown代码块标记
        if result.startswith("```json"):
            result = result[7:]
        if result.endswith("```"):
            result = result[:-3]
        # 移除可能的前后空白字符
        result = result.strip()
        # 尝试修复常见的JSON格式错误
        result = result.replace("'", "\"")

        print(f"处理后的JSON字符串:\n{result}")

        parsed = json.loads(result)
        print(f"解析成功: {parsed}")
        return parsed
    except Exception as e:
        print(f"AI提取失败，错误信息: {e}")
        import traceback
        traceback.print_exc()
        return {
            "name": None,
            "phone": None,
            "email": None,
            "address": None,
            "error": f"AI提取失败: {str(e)}"
        }

def calculate_match_score(resume_text: str, job_description: str) -> dict:
    """计算简历与岗位的匹配度"""
    prompt = f"""
    你是一个专业的招聘面试官。请根据以下岗位需求和简历内容，给出客观公正的匹配度评分。
    
    岗位需求：
    {job_description}
    
    简历内容：
    {resume_text[:4000]}
    
    请严格按照以下JSON格式返回结果：
    {{
        "overall_score": 0-100的整数,
        "skill_match": {{
            "score": 0-100,
            "matched_skills": ["匹配的技能1", "匹配的技能2"],
            "missing_skills": ["缺失的技能1", "缺失的技能2"]
        }},
        "experience_match": {{
            "score": 0-100,
            "analysis": "工作经验匹配度分析，100字以内"
        }},
        "education_match": {{
            "score": 0-100,
            "analysis": "学历背景匹配度分析，50字以内"
        }},
        "summary": "综合评价和建议，150字以内"
    }}
    
    评分标准：
    - 90-100分：非常匹配，完全符合所有要求
    - 70-89分：比较匹配，大部分要求符合
    - 50-69分：基本匹配，部分要求符合
    - 0-49分：不太匹配，大部分要求不符合
    
    只返回JSON，不要任何其他解释！
    """
    
    try:
        result = call_qwen(prompt)
        result = result.strip()
        if result.startswith("```json"):
            result = result[7:]
        if result.endswith("```"):
            result = result[:-3]
        result = result.strip()
        result = result.replace("'", "\"")
        return json.loads(result)
    except Exception as e:
        print(f"匹配度计算失败: {e}")
        return {
            "overall_score": 0,
            "error": f"匹配度计算失败: {str(e)}"
        }
