import base64
from Crypto.Cipher import DES, DES3

# 待解密的 Base64 字符串
enc_b64 = "L89VjHns07U="
enc_bytes = base64.b64decode(enc_b64)  # 解码成字节

# 假设密钥（需要知道密钥才能解密，这里举例用 '12345678'）
des_key = b"12345678"       # DES 8 字节
des3_key = b"123456781234567812345678"  # 3DES 24 字节

# DES 解密（ECB模式）
des_cipher = DES.new(des_key, DES.MODE_ECB)
try:
    des_decrypted = des_cipher.decrypt(enc_bytes)
    print("DES 解密结果:", des_decrypted)
except Exception as e:
    print("DES 解密失败:", e)

# 3DES 解密（ECB模式）
des3_cipher = DES3.new(des3_key, DES3.MODE_ECB)
try:
    des3_decrypted = des3_cipher.decrypt(enc_bytes)
    print("3DES 解密结果:", des3_decrypted)
except Exception as e:
    print("3DES 解密失败:", e)
