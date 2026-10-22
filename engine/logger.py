# engine/logger.py
import logging
import os
from datetime import datetime


class Logger:
    """
    日志与状态追踪模块。
    同时输出到控制台和 logs/run.log 文件。
    """

    def __init__(self, log_file: str = "logs/run.log", name: str = "workflow"):
        self.log_file = log_file
        os.makedirs(os.path.dirname(log_file), exist_ok=True)

        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)

        # 避免重复添加 handler
        if not self.logger.handlers:
            formatter = logging.Formatter(
                "%(asctime)s - %(levelname)s - %(message)s"
            )

            # 文件 handler
            file_handler = logging.FileHandler(log_file, encoding="utf-8")
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

            # 控制台 handler
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

    def log(self, message: str, level: str = "info"):
        """记录一条日志。"""
        level = level.lower()
        if level == "debug":
            self.logger.debug(message)
        elif level == "warning":
            self.logger.warning(message)
        elif level == "error":
            self.logger.error(message)
        else:
            self.logger.info(message)

    def log_step(self, step: str, agent: str, detail: str = ""):
        """记录 Workflow 步骤。"""
        msg = f"[STEP] {step} | Agent={agent}"
        if detail:
            msg += f" | {detail}"
        self.logger.info(msg)

    def log_state(self, state):
        """记录当前 Workflow 状态。"""
        self.logger.info(
            f"[STATE] task_id={state.task_id} status={state.status} "
            f"iteration={state.iteration}"
        )

    def log_error(self, error: Exception, context: str = ""):
        """记录错误。"""
        self.logger.error(f"[ERROR] {context} | {type(error).__name__}: {error}")

    def clear(self):
        """清空日志文件。"""
        with open(self.log_file, "w", encoding="utf-8"):
            pass