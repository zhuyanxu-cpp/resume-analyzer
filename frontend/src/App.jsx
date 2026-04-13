import { useState } from 'react';
import axios from 'axios';

// 后端API地址(本地开发用这个)
//const API_BASE_URL = 'http://localhost:8000';
//替换成阿里云公网地址
const API_BASE_URL = "https://resume-yzer-new-crkmwwlaab.cn-hangzhou.fcapp.run";

function App() {
  const [file, setFile] = useState(null);
  const [resumeInfo, setResumeInfo] = useState(null);
  const [jobDescription, setJobDescription] = useState('');
  const [matchResult, setMatchResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile && selectedFile.type === 'application/pdf') {
      setFile(selectedFile);
      setResumeInfo(null);
      setMatchResult(null);
      setError('');
    } else {
      setError('请选择PDF格式的文件');
    }
  };

  const handleUpload = async () => {
    if (!file) return;
    
    setLoading(true);
    setError('');
    
    try {
      const formData = new FormData();
      formData.append('file', file);
      
      const response = await axios.post(`${API_BASE_URL}/api/upload-resume`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      
      setResumeInfo(response.data.resume_info);
    } catch (err) {
      setError(err.response?.data?.detail || '上传失败，请重试');
    } finally {
      setLoading(false);
    }
  };

  const handleMatch = async () => {
    if (!resumeInfo || !jobDescription) return;
    
    setLoading(true);
    setError('');
    
    try {
      const response = await axios.post(`${API_BASE_URL}/api/match-job`, {
        resume_text: JSON.stringify(resumeInfo),
        job_description: jobDescription
      });
      
      setMatchResult(response.data.match_result);
    } catch (err) {
      setError(err.response?.data?.detail || '匹配失败，请重试');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8 px-4">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold text-center text-gray-800 mb-8">
          AI 赋能的智能简历分析系统
        </h1>
        
        {/* 上传区域 */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <h2 className="text-xl font-semibold mb-4">1. 上传简历(PDF)</h2>
          <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center">
            <input
              type="file"
              accept=".pdf"
              onChange={handleFileChange}
              className="hidden"
              id="file-upload"
            />
            <label
              htmlFor="file-upload"
              className="cursor-pointer text-blue-600 hover:text-blue-800"
            >
              {file ? file.name : '点击选择或拖拽PDF文件到这里'}
            </label>
          </div>
          <button
            onClick={handleUpload}
            disabled={!file || loading}
            className="mt-4 bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
          >
            {loading ? '解析中...' : '解析简历'}
          </button>
        </div>
        
        {/* 错误提示 */}
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">
            {error}
          </div>
        )}
        
        {/* 简历信息展示 */}
        {resumeInfo && (
          <div className="bg-white rounded-lg shadow-md p-6 mb-6">
            <h2 className="text-xl font-semibold mb-4">2. 提取的简历信息</h2>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <p><strong>姓名：</strong>{resumeInfo.name || '未提取到'}</p>
                <p><strong>电话：</strong>{resumeInfo.phone || '未提取到'}</p>
                <p><strong>邮箱：</strong>{resumeInfo.email || '未提取到'}</p>
                <p><strong>地址：</strong>{resumeInfo.address || '未提取到'}</p>
              </div>
              <div>
                <p><strong>求职意向：</strong>{resumeInfo.job_intention || '未提取到'}</p>
                <p><strong>期望薪资：</strong>{resumeInfo.expected_salary || '未提取到'}</p>
                <p><strong>工作年限：</strong>{resumeInfo.work_years || '未提取到'}</p>
                <p><strong>学历背景：</strong>{resumeInfo.education || '未提取到'}</p>
              </div>
            </div>
            
            {resumeInfo.projects && resumeInfo.projects.length > 0 && (
              <div className="mt-4">
                <h3 className="font-semibold mb-2">项目经历：</h3>
                <ul className="list-disc pl-5">
                  {resumeInfo.projects.map((project, index) => (
                    <li key={index}>{project}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}
        
        {/* 岗位匹配区域 */}
        {resumeInfo && (
          <div className="bg-white rounded-lg shadow-md p-6 mb-6">
            <h2 className="text-xl font-semibold mb-4">3. 岗位匹配度分析</h2>
            <textarea
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
              placeholder="请输入岗位需求描述..."
              className="w-full h-32 p-3 border border-gray-300 rounded-lg mb-4"
            />
            <button
              onClick={handleMatch}
              disabled={!jobDescription || loading}
              className="bg-green-600 text-white px-6 py-2 rounded-lg hover:bg-green-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
            >
              {loading ? '计算中...' : '计算匹配度'}
            </button>
          </div>
        )}
        
        {/* 匹配结果展示 */}
        {matchResult && (
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-semibold mb-4">4. 匹配结果</h2>
            <div className="mb-4">
              <div className="flex items-center justify-between mb-2">
                <span className="font-semibold">综合匹配度：</span>
                <span className={`text-2xl font-bold ${
                  matchResult.overall_score >= 80 ? 'text-green-600' :
                  matchResult.overall_score >= 60 ? 'text-yellow-600' : 'text-red-600'
                }`}>
                  {matchResult.overall_score}/100
                </span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-4">
                <div
                  className={`h-4 rounded-full ${
                    matchResult.overall_score >= 80 ? 'bg-green-600' :
                    matchResult.overall_score >= 60 ? 'bg-yellow-600' : 'bg-red-600'
                  }`}
                  style={{ width: `${matchResult.overall_score}%` }}
                />
              </div>
            </div>
            
            {matchResult.skill_match && (
              <div className="mb-4">
                <h3 className="font-semibold mb-2">技能匹配：{matchResult.skill_match.score}/100</h3>
                <p><strong>匹配技能：</strong>{matchResult.skill_match.matched_skills?.join(', ') || '无'}</p>
                <p><strong>缺失技能：</strong>{matchResult.skill_match.missing_skills?.join(', ') || '无'}</p>
              </div>
            )}
            
            {matchResult.experience_match && (
              <div className="mb-4">
                <h3 className="font-semibold mb-2">经验匹配：{matchResult.experience_match.score}/100</h3>
                <p>{matchResult.experience_match.analysis}</p>
              </div>
            )}
            
            {matchResult.education_match && (
              <div className="mb-4">
                <h3 className="font-semibold mb-2">学历匹配：{matchResult.education_match.score}/100</h3>
                <p>{matchResult.education_match.analysis}</p>
              </div>
            )}
            
            {matchResult.summary && (
              <div>
                <h3 className="font-semibold mb-2">综合评价：</h3>
                <p>{matchResult.summary}</p>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
