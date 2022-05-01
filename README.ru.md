# selenium-python-crawler

Программа, которая обходит сайт, открывая все локальные ссылки на нём. Написана на python3 + Selenium webdriver. Учебная.

Скрипт написан на [Python 3.6](http://www.python.org/) и использует [Selenium Webdriver](https://www.selenium.dev/) - драйвер для управления броузером, позволяющий имитировать работу человека на нём.

Написан и проверен с драйвером для Opera и браузером Opera v86

## Использование

```
crawler.py [-h] [-I N] [-w N] [-s filename] [-S scheme] [-l logname] [-D filename] sitename
```
```
Необходимые аргументы:
  sitename              имя обследуемого сайта

optional arguments:
  -h, --help            краткая помощь (на английском)
  -I N, --iterations N  количество итераций (обходов сайта)
  -w N, --wait N        задержка (в секундах) перед очередным запросом
  -s filename, --store filename	имя файла, куда сохраняются результаты краулинга в формате json
  -S scheme, --scheme scheme		схема сайта, http or https
  -l logname, --log logname		имя лог-файла
  -D filename, --driver filename	имя файла с Selenium webdriver, по умолчанию /usr/local/bin/operadriver 
```
