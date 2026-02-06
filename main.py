import os
import uvicorn
import random
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, UploadFile
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

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)  # 端口设为8000
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # 优先读平台PORT，默认8000
    uvicorn.run(app, host="0.0.0.0", port=port)

