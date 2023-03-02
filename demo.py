from urllib.parse import urlencode
from api.api      import Utils
from json         import loads
from random       import choice
from requests     import get, post
from sign         import sign
from device       import mssdk
from time         import time
from hashlib      import md5


device  = mssdk.get_device()
number  = input('phone number: ')

params  = Utils.get_params(device, '28.4.3', {
    "support_webview": "1",
    "cronet_version" : "ae513f3c_2022-08-08",
    "ttnet_version"  : "4.1.103.11-tiktok"
})

payload = urlencode({
    "check_register"    : 1,
    "auto_read"         : 1,
    "account_sdk_source": "app",
    "unbind_exist"      : 35,
    "mix_mode"          : 1,
    "mobile"            : Utils.encrypt(number),
    "multi_login"       : 1,
    "type"              : 3731
})

headers = sign(params, payload, device['secDeviceIdToken']) | {
    "x-ss-stub"                 : md5(payload.encode()).hexdigest().upper(),
    "host"                      : "api16-normal-c-useast1a.tiktokv.com",
    "connection"                : "keep-alive",
    "sdk-version"               : "2",
    "passport-sdk-version"      : "19",
    "x-ss-req-ticket"           : str(int(time() * 1000)),
    "x-tt-bypass-dp"            : "1",
    "x-vc-bdturing-sdk-version" : "2.2.1.i18n",
    "x-tt-dm-status"            : "login=0;ct=0;rt=7",
    "content-type"              : "application/x-www-form-urlencoded; charset=UTF-8",
    "x-tt-store-region"         : "us",
    "x-tt-store-region-src"     : "did",
    "x-tt-store-region-uid"     : "none",
    "x-tt-store-region-did"     : "us",
    "user-agent"                : "com.zhiliaoapp.musically/2022804030 (Linux; U; Android 9; fr_FR; SM-G977N; Build/LMY48Z;tt-ok/3.12.13.1)",
}

resp = post(f"https://api16-normal-c-useast1a.tiktokv.com/passport/mobile/send_code/v1/?{params}", headers=headers, data=payload)
print(resp.content)

code = input("Enter code: ")

params  = Utils.get_params(device, '28.4.3', {})
payload = urlencode({
    "mobile"            : Utils.encrypt(number),
    "code"              : Utils.encrypt(code),
    "account_sdk_source": "app",
    "multi_login"       : 1,
    "mix_mode"          : 1,
})

headers = sign(params, payload, device['secDeviceIdToken']) | {
    "x-ss-stub"                 : md5(payload.encode()).hexdigest().upper(),
    "host"                      : "api16-normal-c-useast1a.tiktokv.com",
    "connection"                : "keep-alive",
    "sdk-version"               : "2",
    "passport-sdk-version"      : "19",
    "x-ss-req-ticket"           : str(int(time() * 1000)),
    "x-tt-bypass-dp"            : "1",
    "x-vc-bdturing-sdk-version" : "2.2.1.i18n",
    "x-tt-dm-status"            : "login=0;ct=0;rt=7",
    "content-type"              : "application/x-www-form-urlencoded; charset=UTF-8",
    "x-tt-store-region"         : "us",
    "x-tt-store-region-src"     : "did",
    "x-tt-store-region-uid"     : "none",
    "x-tt-store-region-did"     : "us",
    "user-agent"                : "com.zhiliaoapp.musically/2022804030 (Linux; U; Android 9; fr_FR; SM-G977N; Build/LMY48Z;tt-ok/3.12.13.1)",
}

resp = post(f"https://api16-normal-c-useast1a.tiktokv.com/passport/mobile/sms_login_only/?{params}", headers=headers, data=payload)
print(resp.content)
