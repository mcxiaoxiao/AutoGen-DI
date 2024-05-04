import requests
import json

async def PredictCyl(value,power_type):
    """
    Predicting the mean variance and range of plant utilization rates based on generation type and generation output values

    Args:
        value (str): value of generation output
        power_type (str):  Type of power generation,include 'fd'(Wind power), 'gf'(Hydropower), 'hdrm'(Coal-fired Thermal Power) , 'sdyg'(Hydropower)

    Returns:
        predict_data (dict): 
        {
        "mean": "",(mean value of plant utilization rate)
        "std": "",( variance of plant utilization rate)
        "interval_lower": "",(lower limit of plant utilization rate interval)
        "interval_upper": ""(upper limit of plant utilization rate interval)
        }
    """

    # FastAPI 应用的 URL
    url = 'http://127.0.0.1:8000/cylpredict'

    # 请求参数
    params = {
        'value':  value,
        'power_type': power_type
    }

    response = requests.get(url, params=params)

    # 检查响应状态码
    if response.status_code == 200:
        # 解析 JSON 响应体并返回
        json_response = response.json()
        print(json_response)
        return json_response
    else:
        # 打印错误信息并返回空字典
        print("CYL Failed to get valid response, status code:", response.status_code)
        return {}