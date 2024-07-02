import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
import undetected_chromedriver as uc


load_dotenv()
DRIVER_PATH = os.getenv('DRIVER_PATH')
SCRAPPING_TITLE = os.getenv("SCRAPPING_TITLE")

download_dir = os.getcwd() + f"/data/{SCRAPPING_TITLE}"
if not os.path.exists(download_dir):
    os.mkdir(download_dir)
# options = webdriver.ChromeOptions()
# options.add_experimental_option("prefs", {
#     "download.default_directory": download_dir,
#     "download.prompt_for_download": False,  # 다운로드 프롬프트 비활성화
#     "download.directory_upgrade": True,
#     "plugins.always_open_pdf_externally": True  # PDF 파일 자동 다운로드 활성화
# })
options = uc.ChromeOptions()
options.headless = False
prefs = {
    "plugins.plugins_disabled": ["Chrome PDF Viewer"],
    "plugins.always_open_pdf_externally": True,
    "download.default_directory": "C:\\Users\\Downloads\\test\\"
}
options.add_experimental_option("prefs", prefs)
options.add_argument("--remote-allow-origins=*")


service = Service(executable_path=DRIVER_PATH)
# driver = webdriver(service=service, options=options)
driver = uc.Chrome(use_subprocess=True, options=options)
actions = ActionChains(driver)

# Defines autodownload and download PATH
params = {
    "behavior": "allow",
    "downloadPath": download_dir
}
driver.execute_cdp_cmd("Page.setDownloadBehavior", params)
