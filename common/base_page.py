from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementNotInteractableException
)
from typing import Optional, Union
import logging

from common.locators import LOCATOR_MAP

class BasePage:
    """基础页面类，提供常用的页面操作方法"""
    
    def __init__(self, driver=None, timeout: int = 10):
        self.driver = driver
        self.timeout = timeout
        self.logger = logging.getLogger(__name__)

    def open(self, url: str) -> None:
        """打开指定URL的网页
        
        Args:
            url: 要访问的网页地址
        """
        try:
            self.driver.get(url)
            self.logger.info(f"成功打开页面: {url}")
        except Exception as e:
            self.logger.error(f"打开页面失败: {url}, 错误: {str(e)}")
            raise

    def find_element(self, type: str, value: str, timeout: Optional[int] = None) -> WebElement:
        """查找页面元素
        
        Args:
            type: 定位方式，支持：id, name, tag, class, link, plink, css, xpath
            value: 定位值
            timeout: 等待超时时间（秒）
            
        Returns:
            WebElement: 找到的页面元素
            
        Raises:
            ValueError: 定位方式无效
            TimeoutException: 等待超时未找到元素
        """
        if type not in LOCATOR_MAP:
            raise ValueError(f"不支持的定位方式: {type}")

        wait_timeout = timeout or self.timeout
        try:
            element = WebDriverWait(self.driver, wait_timeout).until(
                EC.presence_of_element_located((LOCATOR_MAP[type], value))
            )
            return element
        except TimeoutException:
            self.logger.error(f"超时未找到元素: {type}={value}")
            self.save_screenshot(f"element_not_found_{type}_{value}")
            raise
        except Exception as e:
            self.logger.error(f"查找元素失败: {type}={value}, 错误: {str(e)}")
            raise

    def click_element(self, type: str, value: str, timeout: Optional[int] = None) -> None:
        """点击页面元素
        
        Args:
            type: 定位方式
            value: 定位值
            timeout: 等待超时时间（秒）
        """
        try:
            element = self.find_element(type, value, timeout)
            WebDriverWait(self.driver, timeout or self.timeout).until(
                EC.element_to_be_clickable((LOCATOR_MAP[type], value))
            )
            element.click()
            self.logger.info(f"成功点击元素: {type}={value}")
        except ElementNotInteractableException:
            self.logger.error(f"元素不可交互: {type}={value}")
            raise
        except Exception as e:
            self.logger.error(f"点击元素失败: {type}={value}, 错误: {str(e)}")
            raise

    def input_text(self, type: str, value: str, text: str, timeout: Optional[int] = None) -> None:
        """向元素输入文本
        
        Args:
            type: 定位方式
            value: 定位值
            text: 要输入的文本
            timeout: 等待超时时间（秒）
        """
        try:
            element = self.find_element(type, value, timeout)
            element.clear()
            element.send_keys(text)
            self.logger.info(f"成功输入文本: {type}={value}, text={text}")
        except Exception as e:
            self.logger.error(f"输入文本失败: {type}={value}, text={text}, 错误: {str(e)}")
            raise

    def hover_element(self, type: str, value: str, timeout: Optional[int] = None) -> None:
        """鼠标悬停在元素上
        
        Args:
            type: 定位方式
            value: 定位值
            timeout: 等待超时时间（秒）
        """
        try:
            element = self.find_element(type, value, timeout)
            ActionChains(self.driver).move_to_element(element).pause(1).perform()
            self.logger.info(f"成功悬停在元素上: {type}={value}")
        except Exception as e:
            self.logger.error(f"鼠标悬停失败: {type}={value}, 错误: {str(e)}")
            raise

    def switch_to_frame(self, identifier: Union[str, int, WebElement]) -> None:
        """切换到指定框架
        
        Args:
            identifier: 框架的标识符（ID、name或WebElement对象）
        """
        try:
            self.driver.switch_to.frame(identifier)
            self.logger.info(f"成功切换到框架: {identifier}")
        except Exception as e:
            self.logger.error(f"切换框架失败: {identifier}, 错误: {str(e)}")
            raise

    def switch_to_window(self, title: str) -> None:
        """切换到指定标题的窗口
        
        Args:
            title: 目标窗口的标题
        """
        try:
            current_window = self.driver.current_window_handle
            for handle in self.driver.window_handles:
                self.driver.switch_to.window(handle)
                if self.driver.title == title:
                    self.logger.info(f"成功切换到窗口: {title}")
                    return
            self.driver.switch_to.window(current_window)
            raise ValueError(f"未找到标题为 {title} 的窗口")
        except Exception as e:
            self.logger.error(f"切换窗口失败: {title}, 错误: {str(e)}")
            raise

    def clear_cookies(self) -> None:
        """清除所有cookies"""
        try:
            self.driver.delete_all_cookies()
            self.logger.info("成功清除所有cookies")
        except Exception as e:
            self.logger.error(f"清除cookies失败: {str(e)}")
            raise

    def save_screenshot(self, name: str) -> None:
        """保存页面截图
        
        Args:
            name: 截图文件名（不需要扩展名）
        """
        try:
            file_path = f'../data/result_pics/{name}.png'
            self.driver.save_screenshot(file_path)
            self.logger.info(f"成功保存截图: {file_path}")
        except Exception as e:
            self.logger.error(f"保存截图失败: {name}, 错误: {str(e)}")
            raise

    def get_element_text(self, type: str, value: str, timeout: Optional[int] = None) -> str:
        """获取元素的文本内容
        
        Args:
            type: 定位方式
            value: 定位值
            timeout: 等待超时时间（秒）
            
        Returns:
            str: 元素的文本内容
        """
        try:
            element = self.find_element(type, value, timeout)
            return element.text
        except Exception as e:
            self.logger.error(f"获取元素文本失败: {type}={value}, 错误: {str(e)}")
            raise

    def is_element_present(self, type: str, value: str, timeout: Optional[int] = None) -> bool:
        """检查元素是否存在
        
        Args:
            type: 定位方式
            value: 定位值
            timeout: 等待超时时间（秒）
            
        Returns:
            bool: 元素是否存在
        """
        try:
            self.find_element(type, value, timeout or 1)
            return True
        except (TimeoutException, NoSuchElementException):
            return False
