import sys
import pytest
from utils.log_utils import my_logger

@my_logger.runtime_logger
def run_tests():
    """运行测试用例"""
    try:
        # 设置pytest运行参数
        args = [
            '-v',  # 详细输出
            '-s',  # 允许打印输出
            'tests'  # 测试用例目录
        ]
        
        # 运行测试用例
        my_logger.logger.info("开始运行测试用例...")
        exit_code = pytest.main(args)
        
        # 输出测试结果
        if exit_code == 0:
            my_logger.logger.success("测试用例全部通过！")
        else:
            my_logger.logger.warning(f"测试完成，但存在失败用例。退出码：{exit_code}")
        
        return exit_code
        
    except Exception as e:
        my_logger.logger.error(f"运行测试用例时发生错误: {str(e)}")
        return 1

if __name__ == '__main__':
    sys.exit(run_tests()) 