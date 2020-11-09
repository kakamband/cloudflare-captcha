from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.proxy import Proxy
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import enum

class CaptchaType(enum.Enum):
    ReCaptchaV2 = enum.auto()
    hCaptcha = enum.auto()

"""
This is only meant for solving a specific type of cloudflare challenge.
If this doesn't work, you probably need to use a different module.
"""
class Cloudflare:
    def __init__(self, url, proxy=None, timeout=10):
        self.url = url.rstrip("/") + "/robots.txt" # prob the lightest page to load
        self.timeout = timeout # used for page, element and redirect timeouts
        self.active = True

        dc = webdriver.DesiredCapabilities.FIREFOX.copy()
        if proxy:
            dc["proxy"] = {
                "proxyType": "manual",
                "httpProxy": proxy,
                "sslProxy": proxy,
            }
        
        options = webdriver.FirefoxOptions()
        options.add_argument("-headless")

        profile = webdriver.FirefoxProfile()
        # saves some time by not loading images and such
        profile.set_preference("permissions.default.stylesheet", 2)
        profile.set_preference("permissions.default.image", 2)

        self._webdriver = webdriver.Firefox(
            firefox_profile=profile,
            options=options,
            desired_capabilities=dc
        )
        self._webdriver.set_page_load_timeout(self.timeout)
        self._webdriver.get(self.url)

        self.type = self._captcha_type()
        if self.type == CaptchaType.hCaptcha:
            WebDriverWait(self._webdriver, self.timeout).until(EC.element_to_be_clickable((By.ID, "cf-hcaptcha-container")))
        elif self.type == CaptchaType.ReCaptchaV2:
            WebDriverWait(self._webdriver, self.timeout).until(EC.element_to_be_clickable((By.ID, "cf-recaptcha-container")))
            
    def __enter__(self):
        return self
    
    def __exit__(self, x, y, z):
        self.close()
            
    def close(self):
        if self.active:
            self.active = False
            self._webdriver.quit()
    
    def _captcha_type(self):
        ct = self._webdriver.find_element_by_name("cf_captcha_kind").get_attribute("value")
        if ct == "h":
            return CaptchaType.hCaptcha
        elif ct == "rc":
            return CaptchaType.ReCaptchaV2
        else:
            raise Exception("Could not identify captcha on page")

    """
    Submits captcha token, and returns (user_agent, cf_clerance) tuple
    """
    def resolve(self, captcha_response: str) -> tuple:
        if self.type == CaptchaType.hCaptcha:
            self._webdriver.execute_script("""
                document.querySelector("[name=h-captcha-response]").innerText = arguments[0]
                document.querySelector(".challenge-form").submit()""", captcha_response)
            
        elif self.type == CaptchaType.ReCaptchaV2:
            self._webdriver.execute_script("""
                document.querySelector("[name=g-recaptcha-response]").innerText = arguments[0]
                document.querySelector(".challenge-form").submit()""", captcha_response)
            
        WebDriverWait(self._webdriver, self.timeout).until(EC.url_changes(self._webdriver.current_url))
        
        user_agent = self._webdriver.execute_script("return navigator.userAgent")
        cf_clearance = self._webdriver.get_cookie("cf_clearance")["value"]
        self.close()
        
        return (user_agent, cf_clearance)
