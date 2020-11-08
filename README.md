# cloudflare-captcha
Python module for solving a specific type of cloudflare captcha challenge.

# Documentation

## Cloudflare(url, proxy=None, timeout=10)
Starts up a headless selenium instance, and loads the webpage.

## Cloudflare.type
Type of challenge. Either CaptchaType.ReCaptchaV2, or CaptchaType.hCaptcha.

## Cloudflare.resolve(captcha_response)
Submits the captcha token, and returns (user_agent, cf_clearance) as a tuple.
