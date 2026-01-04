import requests
import uuid

# 生成一个随机的 UUID
app_id = str(uuid.uuid4())

# 接口地址
url = f"http://127.0.0.1:5002/apps/{app_id}/debug"

# 请求数据 (Form Data)
data = {
    "query": "你好，请介绍一下你自己"
}

try:
    # stream=True 开启流式接收
    response = requests.post(url, data=data, stream=True)
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        print("Response (Streaming):")
        # 逐块读取并打印
        for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
            if chunk:
                print(chunk, end="", flush=True)
        print() # 换行
    else:
        print("Error:", response.text)
except Exception as e:
    print(f"Request failed: {e}")
