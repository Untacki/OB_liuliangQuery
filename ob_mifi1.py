import os
import requests
import json
import urllib.parse

# --- 配置项 ---
# 在青龙面板选择-环境变量-然后添加变量名称WIFI_DEV_NOS，值就填你的设备号，多个设备号用英文 & 符号连接。
# 示例: 86825xxxx&12345xxxx
# 或者一台设备就添加一个变量都行，可以添加多个变量
DEV_NO_LIST_STRING = os.getenv('WIFI_DEV_NOS')

# WECHAT_ROBOT_WEBHOOK: 选填。企业微信机器人的 Webhook 地址，用于接收推送消息。
WECHAT_ROBOT_WEBHOOK = os.getenv('WECHAT_ROBOT_WEBHOOK')

# WXPUSHER_APP_TOKEN: 选填。WxPusher 的 AppToken。
WXPUSHER_APP_TOKEN = os.getenv('WXPUSHER_APP_TOKEN')
# WXPUSHER_UIDS: 选填。你的 WxPusher UID，多个 UID 请用英文 & 符号连接。
WXPUSHER_UIDS = os.getenv('WXPUSHER_UIDS')

# SERVERJANG_SCKEY: 选填。Server酱的 SCKEY，用于微信推送。
SERVERJANG_SCKEY = os.getenv('SERVERJANG_SCKEY')

# BARK_PUSH_URL: 选填。Bark 推送的 URL，用于 iOS 推送。
BARK_PUSH_URL = os.getenv('BARK_PUSH_URL')

# PUSHPLUS_TOKEN: 选填。PushPlus 的 Token，用于微信公众号/企业微信推送。
PUSHPLUS_TOKEN = os.getenv('PUSHPLUS_TOKEN')

# DINGTALK_WEBHOOK: 选填。钉钉机器人 Webhook 地址，用于钉钉群推送。
DINGTALK_WEBHOOK = os.getenv('DINGTALK_WEBHOOK')

# FEISHU_WEBHOOK: 选填。飞书机器人 Webhook 地址，用于飞书群推送。
FEISHU_WEBHOOK = os.getenv('FEISHU_WEBHOOK')



# 控制推送模式：
# 'full' (详细推送，并打印所有可读字段)
# 'simple' (精简推送)
# 'off' (不推送)
PUSH_MODE = 'simple'
# ------------------------------

def push_to_wecom(title, content):
    """通过企业微信机器人推送消息"""
    data = {
        'msgtype': 'text',
        'text': {
            'content': f'【{title}】\n\n{content}'
        }
    }
    try:
        response = requests.post(WECHAT_ROBOT_WEBHOOK, json=data)
        if response.status_code == 200 and response.json().get('errcode') == 0:
            print('--- 消息已成功推送到企业微信机器人。')
        else:
            print(f"--- 推送失败: {response.json().get('errmsg')}")
    except requests.exceptions.RequestException as e:
        print(f"--- 推送失败！{e}")

def push_to_serverjang(title, content):
    """通过 Server酱 推送消息"""
    url = f'https://sctapi.ftqq.com/{SERVERJANG_SCKEY}.send'
    data = {
        'title': title,
        'desp': content.replace('\n', '\n\n')
    }
    try:
        response = requests.post(url, data=data)
        if response.status_code == 200 and response.json().get('code') == 0:
            print('--- 消息已成功推送到 Server酱。')
        else:
            print(f"--- Server酱推送失败: {response.json().get('message')}")
    except requests.exceptions.RequestException as e:
        print(f"--- Server酱推送失败！{e}")

def push_to_bark(title, content):
    """通过 Bark 推送消息"""
    url = f'{BARK_PUSH_URL}/{urllib.parse.quote(title)}/{urllib.parse.quote(content)}'
    try:
        response = requests.get(url)
        if response.status_code == 200 and response.json().get('code') == 200:
            print('--- 消息已成功推送到 Bark。')
        else:
            print(f"--- Bark推送失败: {response.json().get('message')}")
    except requests.exceptions.RequestException as e:
        print(f"--- Bark推送失败！{e}")

def push_to_pushplus(title, content):
    """通过 PushPlus 推送消息"""
    url = 'http://www.pushplus.plus/send'
    data = {
        'token': PUSHPLUS_TOKEN,
        'title': title,
        'content': content.replace('\n', '<br>')
    }
    try:
        response = requests.post(url, data=data)
        if response.status_code == 200 and response.json().get('code') == 200:
            print('--- 消息已成功推送到 PushPlus。')
        else:
            print(f"--- PushPlus推送失败: {response.json().get('msg')}")
    except requests.exceptions.RequestException as e:
        print(f"--- PushPlus推送失败！{e}")

def push_to_dingtalk(title, content):
    """通过钉钉机器人推送消息"""
    data = {
        'msgtype': 'text',
        'text': {
            'content': f"【{title}】\n{content}"
        }
    }
    try:
        response = requests.post(DINGTALK_WEBHOOK, json=data)
        if response.status_code == 200 and response.json().get('errcode') == 0:
            print('--- 消息已成功推送到钉钉机器人。')
        else:
            print(f"--- 钉钉推送失败: {response.json().get('errmsg')}")
    except requests.exceptions.RequestException as e:
        print(f"--- 钉钉推送失败！{e}")

def push_to_feishu(title, content):
    """通过飞书机器人推送消息"""
    data = {
        'msg_type': 'text',
        'content': {
            'text': f"【{title}】\n\n{content}"
        }
    }
    try:
        response = requests.post(FEISHU_WEBHOOK, json=data)
        if response.status_code == 200 and response.json().get('code') == 0:
            print('--- 消息已成功推送到飞书机器人。')
        else:
            print(f"--- 飞书推送失败: {response.json().get('msg')}")
    except requests.exceptions.RequestException as e:
        print(f"--- 飞书推送失败！{e}")
        
def push_to_wxpusher(title, content):
    """通过 WxPusher 推送消息"""
    if not WXPUSHER_APP_TOKEN or not WXPUSHER_UIDS:
        print('--- WxPusher 配置不完整，跳过推送。')
        return

    uids = WXPUSHER_UIDS.split('&')
    url = 'http://wxpusher.zjiecode.com/api/send/message'
    
    data = {
        'appToken': WXPUSHER_APP_TOKEN,
        'content': content,
        'summary': title,
        'contentType': 1,
        'uids': uids
    }
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200 and response.json().get('code') == 1000:
            print('--- 消息已成功推送到 WxPusher。')
        else:
            print(f"--- WxPusher 推送失败: {response.json().get('msg')}")
    except requests.exceptions.RequestException as e:
        print(f"--- WxPusher 推送失败！{e}")

def send_message(title, content):
    """根据配置调用不同的推送服务"""
    if WECHAT_ROBOT_WEBHOOK:
        push_to_wecom(title, content)
    if SERVERJANG_SCKEY:
        push_to_serverjang(title, content)
    if BARK_PUSH_URL:
        push_to_bark(title, content)
    if PUSHPLUS_TOKEN:
        push_to_pushplus(title, content)
    if DINGTALK_WEBHOOK:
        push_to_dingtalk(title, content)
    if FEISHU_WEBHOOK:
        push_to_feishu(title, content)
    if WXPUSHER_APP_TOKEN and WXPUSHER_UIDS:
        push_to_wxpusher(title, content)
    
    if not any([WECHAT_ROBOT_WEBHOOK, SERVERJANG_SCKEY, BARK_PUSH_URL, PUSHPLUS_TOKEN, DINGTALK_WEBHOOK, FEISHU_WEBHOOK, WXPUSHER_APP_TOKEN]):
        print('--- 未配置任何推送环境变量，跳过推送。')

def main():
    if not DEV_NO_LIST_STRING:
        print('❌ 未找到环境变量 WIFI_DEV_NOS，请先在青龙面板中添加。')
        return

    # 1. 获取最新接口地址
    initial_url = 'http://wifi.ruijiadashop.cn/api/Card/loginCard'
    latest_url = initial_url
    print('--- 🔎 正在获取最新接口地址... ---')
    try:
        response = requests.head(initial_url, allow_redirects=True)
        latest_url = response.url
        print(f'✅ 已获取到最新接口地址: {latest_url}\n')
    except requests.exceptions.RequestException as e:
        print('❌ 获取最新接口地址失败，请检查网络或初始URL。')
        print(f'💬 错误信息: {e}')

    dev_no_list = DEV_NO_LIST_STRING.split('&')
    
    # 2. 遍历设备并查询
    for dev_no in dev_no_list:
        print(f'--- 🚀 开始查询设备 [{dev_no}] 流量... ---')
        push_content = None
        push_title = ''

        try:
            data = {'dev_no': dev_no, 'type': 2}
            headers = {
                 'Content-Type': 'application/json'
                # 'Accept': '*/*',
                # 'Origin': 'http://gdey.ruijiadashop.cn',
                # 'Referer': 'http://gdey.ruijiadashop.cn/index.html',
                # 'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.5 Mobile/15E148 Safari/604.1'
            }
            response = requests.post(
                latest_url,
                json=data,
                headers=headers,
                allow_redirects=True
            )
            response.raise_for_status()
            res_data = response.json()
            
            if res_data.get('code') == 1 and res_data.get('data'):
                # 数据处理与格式化
                info = res_data['data']
                equipment = info.get('equipment', {})
                
                # 处理流量数据，如果缺失则显示提示
                total_amount = info.get('totalAmount')
                remain_amount = info.get('remainAmount')
                
                total_gb_str = f"{(total_amount / 1024):.2f}" if total_amount is not None else "无总流量信息"
                remain_gb_str = f"{(remain_amount / 1024):.2f}" if remain_amount is not None else "无剩余流量信息"
                used_gb_str = f"{((total_amount - remain_amount) / 1024):.2f}" if total_amount is not None and remain_amount is not None else "无法计算已使用流量"
                
                # 使用三元运算符更新设备状态判断逻辑
                device_status_text = '🟢 在线' if equipment.get('deviceStatus') == 1 else '🔴 离线'

                # 格式化所有可用信息，并对空值进行判断
                def get_value(data_dict, key, default_text):
                    value = data_dict.get(key)
                    return value if value is not None and value != '' else default_text

                output_lines = [
                    "--- 📋 查询结果详细信息 ---",
                    f"套餐名称: {get_value(info, 'packageName', '无套餐信息')}",
                    f"使用网络: {get_value(info, 'operator', '无网络信息')}",
                    f"套餐描述: {get_value(info, 'packageDescribe', '无描述信息')}",
                    f"总流量: {total_gb_str} GB",
                    f"剩余流量: {remain_gb_str} GB",
                    f"已使用流量: {used_gb_str} GB",
                    f"到期时间: {get_value(info, 'expiretime', '无到期时间信息')}",
                    f"设备号: {get_value(equipment, 'dev_no', '无设备号')}",
                    f"设备状态: {device_status_text}",
                    f"设备电量: {get_value(equipment, 'devicePower', '无电量信息')}%",
                    f"最后上报时间: {get_value(equipment, 'reportTime', '无上报时间信息')}",
                    f"运行时长: {get_value(equipment, 'runningTime', '无运行时长信息')}",
                    f"热点名称: {get_value(equipment, 'hotspotName', '无热点名称')}",
                    f"热点密码: {get_value(equipment, 'hotspotPassword', '无热点密码')}",
                    "--- 💳 流量卡列表 ---"
                ]

                if equipment.get('card_list'):
                    for i, card in enumerate(equipment['card_list']):
                        card_status_text = '🟢 使用中' if card.get('currentUsage') == 1 else '🔴 未使用'
                        output_lines.append(f"  卡片 {i+1}:")
                        output_lines.append(f"    运营商: {get_value(card, 'operator_text', '无运营商信息')}")
                        output_lines.append(f"    状态: {card_status_text}")
                        output_lines.append(f"    实名状态: {get_value(card, 'realname_status_text', '无实名状态')}")
                        output_lines.append(f"    ICCID: {get_value(card, 'iccid', '无ICCID')}")
                else:
                    output_lines.append("  无流量卡信息")
                
                # print('\n'.join(output_lines))
                
                # 推送内容格式化
                push_title = f"欧本设备 [{dev_no}] 流量查询成功"
                if PUSH_MODE == 'full':
                    push_content = (
                        f"✨ 流量卡查询结果\n\n"
                        f"套餐名称: 【{get_value(info, 'packageName', '无套餐信息')}】\n"
                        f"使用网络: 【{get_value(info, 'operator', '无网络信息')}】\n"
                        f"到期时间: {get_value(info, 'expiretime', '无到期时间信息')}\n\n"
                        f"--- 🚀 流量详情 ---\n"
                        f"总流量: 【{total_gb_str} GB】\n"
                        f"剩余流量: 【{remain_gb_str} GB】\n"
                        f"已使用流量: {used_gb_str} GB\n\n"
                        f"--- 📱 设备信息 ---\n"
                        f"设备号: 【{get_value(equipment, 'dev_no', '无设备号')}】\n"
                        f"设备状态: {device_status_text}\n"
                        f"设备电量: {get_value(equipment, 'devicePower', '无电量信息')}%"
                        f"最后上报时间: {get_value(equipment, 'reportTime', '无上报时间信息')}\n"
                        f"运行时长: {get_value(equipment, 'runningTime', '无运行时长信息')}\n"
                        f"热点名称: {get_value(equipment, 'hotspotName', '无热点名称')}\n"
                        f"热点密码: {get_value(equipment, 'hotspotPassword', '无热点密码')}\n"
                    )

                    if equipment.get('card_list'):
                        push_content += "\n--- 💳 流量卡详情 ---\n"
                        for i, card in enumerate(equipment['card_list']):
                            card_status_text = '🟢 使用中' if card.get('currentUsage') == 1 else '🔴 未使用'
                            push_content += f"‣ 卡片 {i + 1}：\n"
                            push_content += f"  运营商：{get_value(card, 'operator_text', '无运营商信息')}\n"
                            push_content += f"  状态：{card_status_text}\n"
                            push_content += f"  实名：{get_value(card, 'realname_status_text', '无实名状态')}\n"
                            push_content += f"  ICCID：{get_value(card, 'iccid', '无ICCID')}\n"
                    else:
                        push_content += "\n--- 💳 流量卡详情 ---\n"
                        push_content += "  无流量卡信息\n"

                elif PUSH_MODE in ['simple', 'on']:
                    push_content = (
                        f"✨ 流量卡查询结果\n\n"
                        f"使用网络: {get_value(info, 'operator', '无网络信息')}\n"
                        f"套餐名称: {get_value(info, 'packageName', '无套餐信息')}\n"
                        f"总流量: {total_gb_str} GB\n"
                        f"剩余流量: {remain_gb_str} GB\n"
                        f"已使用: {used_gb_str} GB\n\n"
                        f"设备号: {dev_no}\n"
                        f"设备状态: {device_status_text}\n"
                        f"最后上报时间: {get_value(equipment, 'reportTime', '无上报时间信息')}\n"
                    )
            else:
                print('❌ 登录失败！')
                error_msg = res_data.get('msg', '未知错误')
                print(f'💬 错误信息: {error_msg}')
                push_title = f'设备 [{dev_no}] 流量查询失败'
                push_content = f'设备 [{dev_no}] 登录失败！ {error_msg}'
        
        except requests.exceptions.RequestException as e:
            print('❌ 请求出错！')
            error_msg = f'错误: {e}'
            if e.response:
                error_msg = f'状态码: {e.response.status_code}, 错误: {e.response.text}'
            print(f'💬 {error_msg}')
            push_title = f'设备 [{dev_no}] 流量查询失败'
            push_content = f'设备 [{dev_no}] 请求出错！ {e.response.text}'
        finally:
            if PUSH_MODE != 'off' and push_content:
                send_message(push_title, push_content)
            else:
                print('--- 推送模式关闭或配置缺失，跳过推送。')
            print('--- ✅ 任务结束 ---\n')

if __name__ == "__main__":

    main()
