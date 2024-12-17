import time
from selenium import webdriver
from utils.log_utils import my_logger
from common.base_page import BasePage

@my_logger.runtime_logger_class
class TestBaiduSearch:
    """百度搜索测试用例类"""
    
    def setup_class(self):
        """测试类初始化"""
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
        self.page = BasePage(driver=self.driver)
        self.base_url = "https://www.baidu.com"
    
    def teardown_class(self):
        """测试类清理"""
        if self.driver:
            self.driver.quit()
    
    def test_baidu_search(self):
        """测试百度搜索功能"""
        # 打开百度首页
        self.page.open(self.base_url)
        
        # 等待搜索框加载
        search_input = self.page.find_element("id", "kw")
        assert search_input is not None, "未找到搜索输入框"
        
        # 输入搜索关键词
        self.page.input_text("id", "kw", "Selenium 自动化测试")
        
        # 点击搜索按钮
        self.page.click_element("id", "su")
        
        # 等待搜索结果加载
        time.sleep(2)
        
        # 验证搜索结果
        # 检查是否存在搜索结果
        assert self.page.is_element_present("id", "content_left"), "未找到搜索结果"
        
        # 获取并验证页面标题
        assert "Selenium 自动化测试" in self.driver.title, "页面标题不符合预期"
    
    def test_baidu_search_suggestions(self):
        """测试百度搜索建议功能"""
        # 打开百度首页
        self.page.open(self.base_url)
        
        # 在搜索框中输入部分关键词
        self.page.input_text("id", "kw", "pyth")
        
        # 等待搜索建议出现
        time.sleep(1)
        
        # 验证搜索建议是否出现
        assert self.page.is_element_present("id", "form"), "未找到搜索建议"
    
    def test_baidu_homepage_elements(self):
        """测试百度首页基本元素"""
        # 打开百度首页
        self.page.open(self.base_url)
        
        # 检查页面基本元素
        elements_to_check = {
            "搜索框": ("id", "kw"),
            "搜索按钮": ("id", "su"),
            "新闻链接": ("xpath", "//a[contains(text(),'新闻')]"),
            "地图链接": ("xpath", "//a[contains(text(),'地图')]")
        }
        
        for element_name, (locate_type, locate_value) in elements_to_check.items():
            assert self.page.is_element_present(locate_type, locate_value), f"未找到{element_name}" 