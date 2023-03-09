# fintechMeetup-scrapper

## Choose your broswer

The only neccesary thing to modify in order to use the script are the 2 variables at the top of the script:
```python3
driver_path = "/opt/brave.com/chromedriver"
browser_path = "/opt/brave.com/brave/brave"
```
It is necessary to replace the browser_path with the path of your chrome based browser binary.
and also download the chromedriver for your browser's version from the webpage: https://chromedriver.chromium.org/downloads

## Dependencies

This scripts uses *selenium*, you can install it with:
```bash
pip3 install selenium
```
## Run

To run the 2.6K scrapper:
```bash
./the_scrap_2.6k.py
# or
python3 the_scrap_2.6.py
```
To run the Priority lists scrapper:
```bash
./the_scrap.py
# or
python3 the_scrap.py
```
