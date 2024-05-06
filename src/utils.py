import re
import json
import requests
import warnings


# 检查字符串是否以数字结尾
def is_digit_end(s: str):
    # 返回 True 如果 s 是字符串且长度大于0，且最后一个字符是数字
    return isinstance(s, str) and len(s) > 0 and s[-1].isdigit()


# 获取详细地址信息，包含集配站地址解析
def get_detail_address(address_str):
    try:
        # 发送请求到集配站地址解析服务
        url = "http://g.jsf.jd.local/com.jd.wl.wurui.api.open.customer.business.GeoJsfService/map/getJDRegionInfoClue/47405"
        datas = json.dumps([address_str, "1"])  # 构造请求数据
        r = requests.post(url, data=datas, headers={"token": "WREFDJ34"})  # 发送POST请求
        return_dict = json.loads(s=r.text)  # 解析返回的JSON数据

        # 提取省份、城市、区域、经纬度等信息
        province = return_dict["data"].get("province", '')
        city = return_dict["data"].get("city", '')
        distinct = return_dict["data"].get("distinct", '')
        longitude = return_dict["data"].get("longitude", -1)
        latitude = return_dict["data"].get("latitude", -1)

        # 解析集配站信息
        site_json_0 = return_dict["data"].get('siteJson', '')
        site_name = ""
        if site_json_0 != '':
            site = json.loads(site_json_0)
            site_name = site.get("stationName", '') if site else ''
            road = site.get("road", '') if site else ''

        # 解析集配站地址信息
        collection_json_0 = return_dict["data"].get('jipeiJson', '')
        if collection_json_0 != '':
            collection = json.loads(collection_json_0)
            collection_name = collection.get("stationName", '') if collection else ''
            collection_road = collection.get("road", '') if collection else ''

        # 判断集配站名称是否存在，若存在返回True，否则返回False
        return True if site_name not in ['', '无结果'] else False
    except Exception as e:
        # 若发生异常，返回False
        warnings.warn(f"{e}")
        return False


def output_json_data(json_reply: str) -> dict:
    """
    将修正后的JSON字符串转换为字典格式输出。

    参数:
    json_reply: str - 需要修正并转换的JSON字符串。

    返回:
    dict - 转换后的字典对象。

    注意:
    该函数将JSON字符串中的特定标记替换为正确的JSON括号，
    然后尝试解析字符串为字典。如果解析失败，返回一个空字典。
    """
    # 替换JSON字符串中的特殊标记为正确的括号
    try:
        # 尝试将修正后的字符串解析为字典
        data = json.loads(json_reply)
    except Exception as e:
        # 如果解析失败，则返回一个空字典
        warnings.warn(f"json 解析识别 {e}")
        data = {}

    return data


def extract_arabic_numbers(input_string):
    """
    从输入字符串中提取所有阿拉伯数字，并以字符串列表形式返回。

    参数:
    input_string: str - 需要提取数字的字符串。

    返回:
    list of str - 包含所有提取出的数字字符串的列表。

    注意:
    该函数使用正则表达式匹配字符串中的阿拉伯数字，但不将它们转换为整数。
    如果需要整数形式的列表，请取消注释相应的列表推导式。
    """
    # 正则表达式匹配输入字符串中的所有阿拉伯数字，并存储为字符串列表
    numbers = re.findall(r'\d+', input_string)
    # 如果需要将数字字符串转换为整数，请取消注释以下代码行
    # numbers = [int(num) for num in numbers]
    return numbers


def match_phone_and_landline_numbers(text):
    """
    在给定文本中匹配并提取所有手机号码和座机号码。

    参数:
    text: str - 需要搜索号码的文本。

    返回:
    list of str - 包含所有匹配的手机和座机号码的列表。

    注意:
    手机号码匹配模式支持国际格式（如: +86）和国内常见格式，
    座机号码匹配模式支持常见区号-号码格式。
    """
    # 匹配手机号码的正则表达式模式（包括国际格式和国内格式）
    phone_pattern = r'(?:\+?86 ?-?)?1[3-9]\d{9}'
    # 匹配座机号码的正则表达式模式（三位区号-八位号码或四位区号-七位号码）
    landline_pattern = r'\d{3}-\d{8}|\d{4}-\d{7}'

    # 使用正则表达式查找所有匹配的手机和座机号码，并将它们合并为一个列表返回
    numbers = list(re.findall(phone_pattern, text)) + list(re.findall(landline_pattern, text))

    return numbers


def encrypt(string):
    """
    对给定字符串进行简单的加密操作。

    参数:
    string: str - 需要加密的原始字符串。

    返回:
    str - 加密后的字符串。

    加密逻辑:
    如果字符串长度大于等于4，则保留首尾部分，中间部分用"****"替换；
    如果字符串长度小于4，则保留前半部分，后半部分用"x"填充。
    """
    length = len(string)
    # 如果字符串长度大于等于4，则处理中间部分
    if length >= 4:
        mid_start = (length - 4) // 2  # 计算中间部分开始的位置
        mid_end = mid_start + 4  # 计算中间部分结束的位置
        encrypted = string[:mid_start] + "****" + string[mid_end:]  # 替换中间部分为"****"
    else:
        # 如果字符串长度小于4，则处理较短字符串的情况
        mid = length // 2  # 计算字符串的中间位置
        encrypted = string[:mid] + "*" * (length - mid)  # 从中间位置开始，用"x"填充剩余部分

    return encrypted


def trim_string(s, signal=('{', '}')) -> str:
    """
    去除字符串`s`首尾的无关内容。

    参数:
    s (str): 需要处理的字符串。
    signal (tuple, 可选): 两个字符串组成的元组，分别表示要查找的开始和结束信号。默认值为`('{', '}')`。

    返回:
    str: 处理后的字符串，如果未找到开始或结束信号，则返回空字符串。
    """
    # 查找第一个开始信号的索引
    start_index = s.find(signal[0])
    # 如果未找到指定的开始信号，尝试查找默认的'{'
    if start_index == -1:
        start_index = s.find('{')
        if start_index == -1:
            return ""

    # 查找最后一个结束信号的索引
    end_index = s.rfind(signal[1])
    # 如果未找到指定的结束信号，尝试查找默认的'}'
    if end_index == -1:
        end_index = s.find('}')
        if end_index == -1:
            return ""

    # 返回裁剪后的字符串
    return s[start_index:end_index + len(signal[1])]


if __name__ == "__main__":
    pass
