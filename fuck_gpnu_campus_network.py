import re
import urllib.parse
import requests

student_id = '学号'
password = '密码'


def main():
    print("测试网络连接...")
    try:
        # 测试网络是否已连接
        response = requests.get("http://baidu.com", timeout=10)

        # 检查是否已认证
        if "http://www.baidu.com/" in response.text:
            print("网络已连接。")
            return

        print("网络连接失败，尝试认证...")
        # 获取认证所需的查询字符串
        print("获取认证参数...")
        match = re.search(
            rf"top\.self\.location\.href='https://ruijieportal.gpnu.edu.cn:8443/eportal/index\.jsp\?([^']+)'",
            response.text
        )

        if not match:
            print("错误：无法获取认证参数")
            return

        # 处理查询字符串
        query_string = match.group(1)

        # 构建登录参数
        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0",
            "Referer": f"http://10.0.6.247/eportal/index.jsp?{query_string}",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
        }

        post_data = {
            "userId": student_id,
            "password": password,
            "service": "",
            "queryString": urllib.parse.quote(query_string, safe=''),
            "operatorPwd": "",
            "operatorUserId": "",
            "validcode": "",
            "passwordEncrypt": "false"
        }

        # 发送登录请求
        print("尝试登录...")

        login_response = requests.post(
            "http://10.0.6.247/eportal/InterFace.do?method=login",
            data=post_data,
            headers=headers,
            timeout=100
        )

        # 处理登录结果
        if '"result":"success"' in login_response.text:
            print("登录成功。")
        else:
            print("登录失败。错误信息：")
            error_match = re.search(r'"message":"([^"]*)"', login_response.text)
            print(error_match.group(1).encode('latin-1').decode('utf-8'))

    except requests.exceptions.RequestException as e:
        print(f"网络请求错误：{str(e)}")


if __name__ == "__main__":
    main()
