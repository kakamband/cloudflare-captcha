# cloudflare-captcha
Python3 module for solving a specific type of cloudflare captcha challenge.

# Setup
1. `pip install -r requirements.txt`
2. Download the latest release of [geckodriver](https://github.com/mozilla/geckodriver/releases), and place it in the same folder as *captcha_cf.py*

# Usage
```python
from captcha_cf import Cloudflare, CaptchaType
from twocaptcha import TwoCaptcha

# create 2captcha session
solver = TwoCaptcha("API_KEY")

# create cf session
cl = Cloudflare(url="https://v3rmillion.net/",
                proxy=None)

# request token from 2captcha
if cl.type == CaptchaType.hCaptcha:
    ct = solver.hcaptcha(sitekey="45fbc4de-366c-40ef-9274-9f3feca1cd6c",
                         url=cl.url)["code"]

# submit captcha token and get the result
user_agent, cf_clearance = cl.resolve(ct)
print(user_agent, cf_clearance)
```

# Documentation

## Cloudflare(url, proxy=None, timeout=10)
Starts up a headless selenium instance, and loads the webpage.

## Cloudflare.resolve(captcha_response)
Submits the captcha token, and returns (user_agent, cf_clearance) as a tuple.

## Cloudflare.type
Type of challenge. Either CaptchaType.ReCaptchaV2, or CaptchaType.hCaptcha.

## Cloudflare.url
Current page url of the webdriver.
