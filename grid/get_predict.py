import requests


async def PredictFd(now_date, predict_date, original_data ,power_type):
    """
    get power generation forecasts based on current and forecast dates and generation types original_data

    Args:
        now_date (str): date now,format is'yyyymmdd'
        predict_date (str): forecast date ,format is'yyyymmdd'
        original_data (str): generation output values
        power_type (str):  Type of power generation,include '供电', '光伏', '风力'

    Returns:
        predict_data (dict): {"predict":(float)}。
    """

    # FastAPI 应用的 URL
    url = 'http://127.0.0.1:8000/predict'

    # 请求参数
    params = {
        'value':  original_data,
        'start_date': now_date,
        'end_date': predict_date,
        'power_type': power_type
    }

    print(params)

    # 发送 GET 请求
    response = requests.get(url, params=params)


    if response.status_code == 200:
        # 打印响应内容
        print(response.json())
        return response.json()
    else:
        # 打印错误信息并返回空字典
        print("FD Failed to get valid response, status code:", response.status_code)
        return {}
