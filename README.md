# selenium-python-crawler
Site crawer on python3 + Selenium webdriver. For educational purpose

This script written on [Python 3.6](http://www.python.org/) and use [Selenium Webdriver](https://www.selenium.dev/).

I test it with Opera v86 web browser

## Usage

```
crawler.py [-h] [-I N] [-w N] [-s filename] [-S scheme] [-l logname] [-D filename] sitename
```
```
positional arguments:
  sitename              name of processed site

optional arguments:
  -h, --help            show this help message and exit
  -I N, --iterations N  number or iterations
  -w N, --wait N        wait (sec) before http request
  -s filename, --store filename		name of dictionary file
  -S scheme, --scheme scheme		scheme, http or https
  -l logname, --log logname		name of log file
  -D filename, --driver filename	name Selenium webdriver file
```
