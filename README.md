# cloudflare-captcha
Selenium-based module for solving a specific type of cloudflare captcha challenge.

# Setup
1. `pip install -r requirements.txt`
2. Download the latest release of [geckodriver](https://github.com/mozilla/geckodriver/releases), and place it in the same folder as *captcha_cf.py*

# Usage
```python
from captcha_cf import Cloudflare, CaptchaType
from twocaptcha import TwoCaptcha
import requests

solver = TwoCaptcha("API_KEY")

with Cloudflare("https://v3rmillion.net/", proxy=None) as cf:
  cf.setup()
  # request token from 2captcha
  if cf.type == CaptchaType.hCaptcha:
      captcha_token = solver.hcaptcha(
        sitekey="45fbc4de-366c-40ef-9274-9f3feca1cd6c",
        url=cf.url)["code"]
   
  user_agent, cf_clearance = cf.resolve(captcha_token)

with requests.Session() as s:
    s.headers.update({"User-Agent": user_agent})
    s.cookies.update({"cf_clearance": cf_clearance})

    r = s.get("https://v3rmillion.net/")
    print(r.text)
```

# Documentation

## Cloudflare(url, proxy=None, timeout=10, user_agent=None)
Starts up a headless selenium instance, and loads the webpage.

## Cloudflare.resolve(captcha_response)
Submits the captcha token, and returns (user_agent, cf_clearance) as a tuple.

## Cloudflare.type
Type of challenge. Either CaptchaType.ReCaptchaV2, or CaptchaType.hCaptcha.

## Cloudflare.url
Current page url of the webdriver.
