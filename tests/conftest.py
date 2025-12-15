# tests/conftest.py
import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

@pytest.fixture
def sample_bot():
    """Фикстура для тестового бота"""
    from bot import EnhancedFAQBot
    return EnhancedFAQBot(faq_dict={
        "тест1": "ответ1",
        "тест2": "ответ2"
    })