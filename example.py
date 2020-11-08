from captcha_cf import Cloudflare, CaptchaType
from twocaptcha import TwoCaptcha

# create 2captcha session
solver = TwoCaptcha("API_KEY")

# create session
cl = Cloudflare(url="https://v3rmillion.net/",
                proxy=None)

# get token for captcha
if cl.type == CaptchaType.hCaptcha:
    ct = solver.hcaptcha(sitekey="45fbc4de-366c-40ef-9274-9f3feca1cd6c",
                         url=cl.url)["code"]

# get result
user_agent, cf_clearance = cl.resolve(ct)

print(user_agent, cf_clearance)