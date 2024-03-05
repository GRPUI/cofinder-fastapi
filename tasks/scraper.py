# from celery import Celery
import undetected_chromedriver as webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
import selenium
import dotenv
import os
import dns_scraper
from multiprocessing import Pool


def main() -> None:
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    options.add_experimental_option(
        'prefs',
        {
            'profile.managed_default_content_settings.images': 2,
            'profile.managed_default_content_settings.mixed_script': 2,
            'profile.managed_default_content_settings.media_stream': 2,
            'profile.managed_default_content_settings.stylesheets': 2
        }
    )
    options.add_argument("--incognito")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.page_load_strategy = "eager"

    proxy = Proxy()
    proxy.proxyType = ProxyType.MANUAL
    dotenv.load_dotenv()
    proxy_address = os.getenv("PROXY_ADDRESS")
    proxy.http_proxy = proxy_address
    capabilities = selenium.webdriver.DesiredCapabilities.CHROME

    driver = webdriver.Chrome(options=options, desired_capabilities=capabilities)
    print(
        dns_scraper.get_price(
            driver,
            "https://www.dns-shop.ru/product/48b658653727ed20/141-noutbuk-dexp-aquilon-seryj/"
        )
    )


if __name__ == "__main__":
    pool = Pool(4)
    pool.map(main, range(4))
