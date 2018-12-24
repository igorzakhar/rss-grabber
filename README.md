#  Граббер статей с новостных сайтов

### Тестовое задание на позицию Junior Python Developer ([https://outofcloud.ru/](https://outofcloud.ru/))

### Задача: 
Необходимо реализовать граббер статей с новостных сайтов:

&nbsp;&nbsp;&nbsp;&nbsp;[https://lenta.ru/rss](http://lenta.ru/rss)  
&nbsp;&nbsp;&nbsp;&nbsp;[https://www.interfax.ru/rss.asp](http://www.interfax.ru/rss.asp)  
&nbsp;&nbsp;&nbsp;&nbsp;[https://www.kommersant.ru/RSS/news.xml](http://www.kommersant.ru/RSS/news.xml)  
&nbsp;&nbsp;&nbsp;&nbsp;[https://www.m24.ru/rss.xml](http://www.m24.ru/rss.xml)

### Базовый функционал:
- Получение списка свежих статей из rss-канала заданного источника. Каждый
элемент данного списка представляет собой ссылку, заголовок, краткое
описание, дату публикации.
- Получение содержимого статьи по ссылке заданного источника. Результат
должен содержать заголовок статьи, содержимое статьи в виде списка абзацев
с чистым текстом (без html), ссылку на изображение, которое ассоциируется со
статьей (если такая имеется в источнике).
- Предусмотреть возможность простого расширения списка новостных сайтов.

## Описание
Класс каждого rss-канала создаётся динамически при импорте модуля ```rss_grabber``` и наследует поведение от базового класса ```Feed```([ссылка на код](https://github.com/igorzakhar/rss-grabber/blob/7e5dc0ae2404f7e7b5548b81893fab8fbd694fac/rss_grabber.py#L16)), который реализует общий функционал. Имя класса для  rss-канала основано на доменном имени 2 уровня в url адресе rss-канала. Например, для rss-канала ```https://lenta.ru/rss``` класс будет называться ```Lenta```.
URL-адреса rss-каналов находятся в файле ```rss_feeds.txt```, который имеет вид:
```
https://lenta.ru/rss
https://www.interfax.ru/rss.asp
...
```
Для добавления rss-канала добавте его url-адрес в файл ```rss_feeds.txt```.

## Установка

Для использования модуля потртребуется предустановленный Python 3.5 (на других версиях не проверялся).  
1. Скопируйте файлы ```rss_grabber.py``` и ```rss_feeds.txt``` в каталог с вашим проектом.

2. Создайте и активируйте виртуально окружение, например:
```
$ python3 -m venv my_virtual_environment
$ source my_virtual_environment/bin/activate
```
3. Установите сторонние библиотеки  из файла зависимостей:
```
pip install -r requirements.txt # В качестве альтернативы используйте pip3
```

Рекомендуется устанавливать зависимости в виртуальном окружении, используя [virtualenv](https://github.com/pypa/virtualenv), [virtualenvwrapper](https://pypi.python.org/pypi/virtualenvwrapper) или [venv](https://docs.python.org/3/library/venv.html).

В программе используются следующие сторонние библиотеки:  
- [feedparser](https://pypi.org/project/feedparser/)
- [goose3](https://github.com/goose3/goose3)

## Использование

### Пример для ленты.ру:
Получение списка свежих статей из rss-канала заданного источника: 
```python
>>> from rss_grabber import Lenta
>>> lenta = Lenta()
>>> news = lenta.news(limit=3)
>>> print(news)
[{
'title': "Названы самые ненадежные пароли года",
'link': "https://lenta.ru/news/2018/12/14/password/",
'desc': "Аналитики компании SplashData опубликовали список худших паролей, которые юзеры использовали в 2018 году...",
'published': "14.12.2018 19:33"
}, ... ]
```
Получение содержимого статьи по ссылке заданного источника:  
```python
>>> url = news[0]['link']
>>> data = lenta.grub(url)
>>> print(data)
{
    'title': 'Названы самые ненадежные пароли года',
    'image': 'https://icdn.lenta.ru/images/2018/12/14/15/20181214154954686/detail_bf1773492fa73c50ed2781da480e38a1.jpg',
    'content': ['Аналитики компании SplashData опубликовали список худших паролей, которые юзеры использовали в 2018 году. Результаты исследования размещены на сайте организации.', ..., ...]

}
```

# Цели проекта

Код написан в образовательных целях.
