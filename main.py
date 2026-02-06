import os
import uvicorn
import random
import traceback
import mimetypes  # 新增：用于自动识别文件媒体类型
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, UploadFile, HTTPException  # 新增 HTTPException
from fastapi.responses import FileResponse  # 新增 FileResponse
from pydantic import BaseModel  # 导入 BaseModel

app = FastAPI()

origins = [
    "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.get("/list")  # 路径直接定义为 /list，无需额外参数
async def get_random_id():
    # 生成8位随机数字（10000000-99999999）
    random_id = random.randint(10000000, 99999999)
    #print(f"生成的8位随机数字: {random_id}")
    return random_id  # 直接返回随机数字

# 定义数据模型
class UserInfo(BaseModel):
    name: str
    age: int

# 添加 POST 请求接口
@app.post("/list")
async def post_user_info(list: UserInfo):
    # 生成8位随机数字（10000000-99999999）
    random_id = random.randint(10000000, 99999999)
    return random_id

@app.post("/upload")
async def create_upload_file(file: UploadFile):
    # 1. 定义目标目录（原始字符串避免转义）
    # target_dir = r"E:\ZJK_Python\90_DocuTest"
    target_dir = "./upload_files"  # 容器内相对路径，自动创建在应用根目录
    # 2. 自动创建目录（不存在则创建）
    os.makedirs(target_dir, exist_ok=True)
    # 3. 拼接「目录+文件名」的完整路径
    file_path = os.path.join(target_dir, file.filename)
    
    # 4. 读取文件内容并写入指定路径
    contents = await file.read()
    with open(file_path, "wb") as f:
        f.write(contents)  # 仅写入文件内容，而非路径+内容  
    return {"filename": file.filename, "save_path": file_path}

@app.get("/download")  # 支持动态下载 upload_files 目录下的文件
async def download():  # 新增文件名参数，按需下载指定文件
    # 1. 定义文件存储根目录（和上传接口保持一致）
    file_path = "./upload_files/AAA.png"
    
    try:
        # 检查文件是否存在
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail=f"文件 {filename} 不存在")
        # 检查是否是文件（而非目录）
        if not os.path.isfile(file_path):
            raise HTTPException(status_code=400, detail=f"{filename} 不是有效文件")
        
        # 自动识别文件的媒体类型（替代硬编码）
        media_type, _ = mimetypes.guess_type(file_path)
        # 兜底：如果无法识别类型，按二进制流处理
        if media_type is None:
            media_type = "application/octet-stream"
        
        # 返回文件响应
        return FileResponse(
            path=file_path,
            filename="AAA.png",  # 下载时显示的文件名（和请求的文件名一致）
            media_type="image/png"
        )
    except PermissionError:
        raise HTTPException(status_code=403, detail=f"无权限读取文件 {filename}")
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"下载失败：{str(e)}")

# 兼容原有需求：如需保留固定下载 AAA.png 的接口，可新增以下路由（可选）
@app.get("/download/aaa")
async def download_aaa():
    return await download("AAA.png")

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)  # 端口设为8000
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # 优先读平台PORT，默认8000
    uvicorn.run(app, host="0.0.0.0", port=port)

