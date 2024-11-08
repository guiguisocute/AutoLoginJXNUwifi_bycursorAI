import json
import base64
import hashlib
import requests
import time

class LoginHandler:
    def __init__(self):
        self.base_url = "http://172.17.1.2"
        self.session = requests.Session()
        
        # 定义运营商映射
        self.operator_map = {
            "移动校园宽带": "@cmcc",
            "联通校园宽带": "@unicom",
            "电信校园宽带": "@telecom"
        }
    
    def login(self, username, password, operator="移动校园宽带"):
        # 添加运营商后缀
        if operator in self.operator_map:
            username = username + self.operator_map[operator]
            
        # 获取challenge
        challenge_data = self.get_challenge(username)
        if challenge_data['res'] != "ok":
            return False, "获取challenge失败"
            
        token = challenge_data['challenge']
        ip = challenge_data['client_ip']

        # 构造info
        info = {
            "username": username,
            "password": password,
            "ip": ip,
            "acid": "1",
            "enc_ver": "srun_bx1"
        }
        
        # 加密处理
        encrypted_info = self.encrypt(info)
        
        # 发送登录请求
        login_url = f"{self.base_url}/cgi-bin/srun_portal"
        data = {
            "action": "login",
            "username": username,
            "password": "{MD5}" + password,
            "ac_id": "1",
            "ip": ip,
            "info": encrypted_info,
            "chksum": self.get_chksum(info, token),
            "n": "200",
            "type": "1",
            "_": int(time.time() * 1000)
        }
        
        response = self.session.get(login_url, params=data)
        result = response.json()
        
        if result['res'] == "ok":
            return True, "登录成功"
        else:
            return False, result.get('error_msg', '登录失败')

    def encrypt(self, info):
        def s(a):
            c = len(a)
            v = []
            for i in range(0, c, 4):
                v.append(
                    ord(a[i]) | 
                    (ord(a[i + 1]) << 8 if i + 1 < c else 0) |
                    (ord(a[i + 2]) << 16 if i + 2 < c else 0) |
                    (ord(a[i + 3]) << 24 if i + 3 < c else 0)
                )
            return v

        def l(a, b):
            d = len(a)
            c = (d - 1) << 2
            if b:
                m = a[d - 1]
                if m < c - 3 or m > c:
                    return None
                c = m
            for i in range(d):
                a[i] = chr(a[i] & 0xff) + chr(a[i] >> 8 & 0xff) + \
                       chr(a[i] >> 16 & 0xff) + chr(a[i] >> 24 & 0xff)
            if b:
                return ''.join(a)[:c]
            return ''.join(a)

        def encode(str):
            v = s(str)
            k = s('1234567890')
            n = len(v) - 1
            z = v[n]
            y = v[0]
            c = 0x86014019 | 0x183639A0
            m = 0
            e = 0
            p = 0
            q = 6 + 52 // (n + 1)
            d = 0
            while 0 < q:
                d = d + c & (0x8CE0D9BF | 0x731F2640)
                e = d >> 2 & 3
                for p in range(n):
                    y = v[p + 1]
                    m = z >> 5 ^ y << 2
                    m = m + ((y >> 3 ^ z << 4) ^ (d ^ y))
                    m = m + (k[(p & 3) ^ e] ^ z)
                    v[p] = v[p] + m & (0xEFB8D130 | 0x10472ECF)
                    z = v[p]
                y = v[0]
                m = z >> 5 ^ y << 2
                m = m + ((y >> 3 ^ z << 4) ^ (d ^ y))
                m = m + (k[(n & 3) ^ e] ^ z)
                v[n] = v[n] + m & (0xBB390742 | 0x44C6F8BD)
                z = v[n]
                q = q - 1
            return l(v, False)

        # 将info转换为JSON字符串
        info_str = json.dumps(info)
        encrypted = encode(info_str)
        return "{SRUN3}\r\n" + base64.b64encode(encrypted.encode()).decode()

    def get_chksum(self, info, token):
        # 计算校验和
        info_str = json.dumps(info)
        n = len(info_str)
        i = 0
        value = 0
        
        while n > i:
            value = value * 0x83 + ord(info_str[i]) & 0xFFFFFFFF
            i += 1
            
        value = value * 0x83 + len(info_str) & 0xFFFFFFFF
        value = value * 0x83 + ord('n') & 0xFFFFFFFF
        value = value * 0x83 + ord('x') & 0xFFFFFFFF
        value = value * 0x83 + ord('f') & 0xFFFFFFFF
        
        chkstr = f"{value}{token}"
        return hashlib.sha1(chkstr.encode()).hexdigest() 