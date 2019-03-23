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

## Описание работы модуля
Класс каждого rss-канала наследует поведение от базового класса ```Feed```([ссылка на код](https://github.com/igorzakhar/rss-grabber/blob/7e5dc0ae2404f7e7b5548b81893fab8fbd694fac/rss_grabber.py#L16)), который реализует общий функционал.    
Список rss каналов можно сформировать следующим образом:  
1. Загрузить список каналов из файла с помощью функции **rss_grabber.load_feeds_from_file(filename)**. Функция принимает единственный обязательный аргумент - путь до файла со списком url-адресов rss каналов. Пример файла:  
```
https://lenta.ru/rss
https://www.interfax.ru/rss.asp
https://www.kommersant.ru/RSS/news.xml
https://www.m24.ru/rss.xml
...
...
```
 Имя класса для  rss-канала основано на доменном имени 2 уровня в url адресе rss-канала. Например, для rss-канала ```https://lenta.ru/rss``` класс будет называться ```Lenta```.  
2. Добавлять rss каналы можно по одному с помощью функции **rss_grabber.add_feed(rss_url, name='')**. Функция принимает следующие аргументы:  
- **rss_url** - ссылка на rss канал, обязательный аргумент;  
- **name** - имя класса rss канала, необязательный аргумент, по умолчанию имя класса формируется на основании доменного имени 2 уровня. Например, для rss-канала ```https://lenta.ru/rss``` класс будет называться ```Lenta```.


## Установка

Для использования модуля потртребуется предустановленный Python >= 3.5 (на других версиях не проверялся).
1. Скопируйте файл ```rss_grabber.py``` в каталог с вашим проектом.

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
Например, имеется файл со списком rss каналов следующего содержания:
```
https://lenta.ru/rss
https://www.interfax.ru/rss.asp
```
Загрузка списка rss каналов из файла ```'rss_feeds.txt'```:
```python
>>> import rss_grabber
>>> rss_grabber.load_feeds_from_file('rss_feeds.txt')
```
После загрузки доступ к rss каналам можно получить следующим образом:
```python
>>> lenta = Lenta()
>>> interfax = Interfax() 
```

Добавление rss канала с использованием url-адреса:
```python
>>> rss_grabber.add_feed('https://www.kommersant.ru/RSS/news.xml')
>>> kommers = Kommersant()
>>> news = kommers.news(limit=1)
>>> print(news)
[{'link': 'https://www.kommersant.ru/doc/3922653', 
  'title': '«РИА Новости»: спутник «Глонасс-М» планируют запустить с Плесецка в мае 2019', 
  'published': '23.03.2019 04:19', 
  'desc': 'В середине мая текущего года с космодрома Плесецк планируется запуск космического аппарата «Глонасс-М» для поддержания работы навигационной спутниковой системы ГЛОНАСС, сообщили «РИА Новости» со ссылкой на источник. По его данным, сейчас 16 из 26 спутников, находящихся на орбите, работают за пределами срока службы.«Предварительно, на середину мая запланирован пуск с Плесецка ракеты-носителя "Союз-2.1б" с разгонным блоком "Фрегат" и навигационным спутником "Глонасс-М"»,— сказал источник. Он отметил, что для этого используют один из четырех спутников «Глонасс-М» в наземном резерве.Первый «Глонасс-М» был запущен в 2011 году, его срок активного существования составляет семь лет.Всего вокруг орбиты Земли находится 26 спутников, 23 из них работают по целевому назначению, для глобального покрытия земного шара навигационными сигналами необходимо 24 спутника, работающих по целевому назначению.'}]
```
Получение списка свежих статей из rss-канала заданного источника:
```python
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
