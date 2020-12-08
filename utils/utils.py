import json
import time

daily_format = '今日天气：{}\n气温：\n  最低：{}°C\n  最高：{}°C\n相对湿度：{}%\n空气质量（AQI）：{}\n风力：{}，{}m/s\n紫外线指数：{} ({})'
current_format = '时间：{}\n当前天气：{}\n气温：{}°C\n体感温度：{}°C\n相对湿度：{}%\n空气质量（AQI）：{} ({})\n风力：{}，{}m/s\n紫外线指数：{} ({})'
weather_code = {
    "CLEAR_DAY": "晴（白天）",
    "CLEAR_NIGHT": "晴（夜间）",
    "PARTLY_CLOUDY_DAY": "多云（白天）",
    "PARTLY_CLOUDY_NIGHT": "多云（夜间）",
    "CLOUDY": "阴",
    "LIGHT_HAZE": "轻度雾霾",
    "MODERATE_HAZE": "中度雾霾",
    "HEAVY_HAZE": "重度雾霾",
    "LIGHT_RAIN": "小雨",
    "MODERATE_RAIN": "中雨",
    "HEAVY_RAIN": "大雨",
    "STORM_RAIN": "暴雨",
    "FOG": "雾",
    "LIGHT_SNOW": "小雪",
    "MODERATE_SNOW": "中雪",
    "HEAVY_SNOW": "大雪",
    "STORM_SNOW": "暴雪",
    "DUST": "浮尘",
    "SAND": "沙尘",
    "WIND": "大风"
}

# with open("utils/current.json", 'r') as f:
#     tmp = json.load(f)
# print(tmp)


def dailyWeatherToStr(pack: dict) -> str:
    weather = pack['result']['daily']
    skycon = weather_code[weather['skycon'][0]['value']]
    temperature_min = weather['temperature'][0]['min']
    temperature_max = weather['temperature'][0]['max']
    humidity = weather['humidity'][0]['avg'] * 100
    aqi = weather['air_quality']['aqi'][0]['avg']['chn']
    wind_speed = round(weather['wind'][0]['avg']['speed'] / 3.6, 1)
    wind_direction = windDirectionToStr(weather['wind'][0]['avg']['direction'])
    ultraviolet = weather['life_index']['ultraviolet'][0]['index']
    ultraviolet_info = weather['life_index']['ultraviolet'][0]['desc']
    tmp = daily_format.format(skycon, temperature_min, temperature_max,
                              humidity, aqi, wind_direction, wind_speed,
                              ultraviolet, ultraviolet_info)
    return tmp


def currentWeatherToStr(pack: dict) -> str:
    time_now = timestampToTime(pack['server_time'])
    weather = pack['result']['realtime']
    skycon = weather_code[weather['skycon']]
    temperature = weather['temperature']
    apparent_temperature = weather['apparent_temperature']
    humidity = weather['humidity'] * 100
    aqi = weather['air_quality']['aqi']['chn']
    aqi_info = weather['air_quality']['description']['chn']

    wind_speed = round(weather['wind']['speed'] / 3.6, 1)
    wind_direction = windDirectionToStr(weather['wind']['direction'])

    ultraviolet = weather['life_index']['ultraviolet']['index']
    ultraviolet_info = weather['life_index']['ultraviolet']['desc']

    tmp = current_format.format(time_now, skycon, temperature,
                                apparent_temperature, humidity, aqi, aqi_info,
                                wind_direction, wind_speed, ultraviolet,
                                ultraviolet_info)
    return tmp


def timestampToTime(stamp: float) -> str:
    # 转换成localtime
    time_local = time.localtime(stamp)
    # 转换成新的时间格式(2016-05-05 20:28:54)
    return time.strftime("%Y-%m-%d %H:%M:%S", time_local)


def windDirectionToStr(direction_tmp: float) -> str:
    wind_direction_code = ['正北', '北偏东', '正东', '东偏南', '正南', '南偏西', '正西', '西偏北']
    wind_direction_index = 0
    if 0 < direction_tmp < 90:
        wind_direction_index = 1
    elif direction_tmp >= 90:
        wind_direction_index = 2
        while direction_tmp > 90:
            direction_tmp -= 90
            wind_direction_index += 1
            if direction_tmp >= 90:
                wind_direction_index += 1
    wind_direction = wind_direction_code[wind_direction_index]
    wind_direction += (str(round(direction_tmp, 1)) +
                       '°') if wind_direction_index % 2 != 0 else ''
    return wind_direction


# print(currentWeatherToStr(tmp))
