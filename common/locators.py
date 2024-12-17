from selenium.webdriver.common.by import By
from typing import Dict, Any

class Locator:
    """定位器类型枚举"""
    CSS = By.CSS_SELECTOR
    ID = By.ID
    NAME = By.NAME
    XPATH = By.XPATH
    LINK_TEXT = By.LINK_TEXT
    PARTIAL_LINK_TEXT = By.PARTIAL_LINK_TEXT
    TAG = By.TAG_NAME
    CLASS = By.CLASS_NAME

LOCATOR_MAP: Dict[str, Any] = {
    'css': Locator.CSS,
    'id': Locator.ID,
    'name': Locator.NAME,
    'xpath': Locator.XPATH,
    'link': Locator.LINK_TEXT,
    'plink': Locator.PARTIAL_LINK_TEXT,
    'tag': Locator.TAG,
    'class': Locator.CLASS,
}