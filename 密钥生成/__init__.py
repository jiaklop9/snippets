import jwt
import datetime

# 读取私钥和公钥
with open('private.pem', 'r') as f:
    private_key = f.read()

with open('public.pem', 'r') as f:
    public_key = f.read()

# 需要传递的信息
payload = {
    'iss': 'zhb',  # 签发者
    'iat': int(datetime.datetime.now().timestamp()),  # 签发时间
    'exp': int(datetime.datetime.now().timestamp()) + 3600 * 24 * 365 * 100,  # 过期时间（一小时，可根据需求修改）
    'sub': 'views'  # 即用户名，注意不能写默认用户名admin
}

# 使用私钥生成JWT
token = jwt.encode(payload, private_key, algorithm='RS256')
print('Generated Token:', token)

# 使用公钥验证JWT
try:
    decoded = jwt.decode(token, public_key, algorithms=['RS256'])
    print('Decoded Token:', decoded)
except jwt.ExpiredSignatureError:
    print('Token is expired')
except jwt.InvalidTokenError as e:
    print('Token is invalid:', str(e))
