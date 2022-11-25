from amiyabot import PluginInstance, Message, Chain, Equal
import requests
import datetime
import os
from pathlib import Path

curr = os.path.dirname(__file__)
bot = PluginInstance(
    name='每日新闻',
    version='1.0',
    plugin_id='amiyabot_daily_news',
    plugin_type='',
    description='每日新闻推送,直接发送关键字【新闻】即可触发，无需添加前缀兔兔',
    document=f'{curr}/README.md'
)


def get_daily_news():

    date = datetime.date.today()
    curr_dir = Path.cwd().resolve()
    file = curr_dir / 'resource' / 'daily_news' / f'{date}.jpg'
    print(file)
    if Path(file).exists():
        return str(file)
    else:
        file_dir = curr_dir / 'resource' / 'daily_news'
        if Path(file_dir).exists():
            pass
        else:
            path = Path(file_dir)
            path.mkdir(parents=True, exist_ok=True)
        response = requests.get(url='http://bjb.yunwj.top/php/tp/lj.php', verify=False)
        image_url = response.json()['tp']
        image = requests.get(url=image_url, verify=False)
        with open(file, 'wb') as f:
            f.write(image.content)
        return str(file)


@bot.on_message(keywords=Equal('新闻'), check_prefix=False)
async def _(data: Message):
    target = get_daily_news()
    return Chain(data, at=False).image(target)
