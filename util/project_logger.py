# -*- coding: utf-8 -*-
# @Time     : 2025/09/05
# @Author   : J. Huang
# @Email    : jiachenghuang0601@gmail.com


import logging
import sys
import os
from datetime import datetime


def init_logger(log_dir='logs', task_name=None):
    """
    Initializes the logger with both console and file output.
    Only runs once per process.
    """
    root_logger = logging.getLogger()

    if root_logger.handlers:
        return  # Prevent duplicate logging handlers if called more than once

    root_logger.setLevel(logging.INFO)

    # Create log directory if it doesn't exist
    # One level above the directory where this file lives
    current_file_dir = os.path.dirname(os.path.abspath(__file__))
    project_root_dir = os.path.abspath(os.path.join(current_file_dir, os.pardir))
    log_dir = os.path.join(project_root_dir, 'logs')
    os.makedirs(log_dir, exist_ok=True)

    # Generate log filename with optional task name
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    base_name = f"{task_name}_" if task_name else ""
    log_filename = f"{base_name}{timestamp}.log"
    log_path = os.path.join(log_dir, log_filename)

    formatter = logging.Formatter(
        '[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # File handler
    file_handler = logging.FileHandler(log_path, encoding='utf-8')
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)

    # Optional: log that logging is initialized
    logging.getLogger(__name__).info(f"Logger initialized. Log file: {log_path}")
