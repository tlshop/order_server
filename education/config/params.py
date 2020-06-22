

import os


"""
支付宝支付
"""
AliPay_signature = os.getenv("AliPay_signature","")
AliPay_Appid = os.getenv("AliPay_Appid","")
Alipay_callbackUrl = os.getenv("Alipay_callbackUrl","")
Alipay_callbackUrlForVip = os.getenv("Alipay_callbackUrlForVip","")
AliPay_app_private_key = os.getenv("AliPay_app_private_key","")
AliPay_alipay_public_key = os.getenv("AliPay_alipay_public_key","")
AliPay_way = os.getenv("AliPay_way","https://openapi.alipaydev.com/gateway.do")