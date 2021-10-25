
import telegram
import requests
from bs4 import BeautifulSoup
from apscheduler.schedulers.blocking import BlockingScheduler

year = '2021'
month = '10'
day = '31'
date = year + month + day
url = 'http://www.cgv.co.kr/common/showtimes/iframeTheater.aspx?areacode=01&theatercode=0013&date='
telegram_token = ''  # telegram bot token
telegram_id = ''  # telegram user id
telegram_bot = telegram.Bot(token=telegram_token)
count = 0
interval_minute = 5  # every 5 min


def get_movie_info():
    html = requests.get(url + date)
    soup = BeautifulSoup(html.text, 'html.parser')
    imax = soup.select_one('span.imax')

    if imax:
        parent = imax.find_parent('div', class_='col-times')
        title = parent.select_one('div.info-movie > a > strong').text.strip()
        message = year + '/' + month + '/' + day + ' <' + title + '>' + ' IMAX 예매가 열렸습니다.'
        # print(message)
        telegram_bot.sendMessage(chat_id=telegram_id, text=message)

    global count
    count += 1

    if count * interval_minute >= 60:
        count = 0
        if imax:
            pass
        else:
            message = year + '/' + month + '/' + day + ' IMAX 예매가 아직 열리지 않았습니다.'
            telegram_bot.sendMessage(chat_id=telegram_id, text=message)


if __name__ == '__main__':
    '''
    for i in telegram_bot.getUpdates():
        print(i.message)
    '''
    schedule = BlockingScheduler()
    schedule.add_job(get_movie_info, 'interval', minutes=interval_minute, misfire_grace_time=None)
    schedule.start()
