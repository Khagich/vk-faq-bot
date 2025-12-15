# tests/test_bot_basic.py
import sys
import os
import pytest

# Добавляем src в путь
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from bot import EnhancedFAQBot

class TestEnhancedFAQBot:
    """Тесты базовой функциональности бота"""
    
    def setup_method(self):
        """Настройка перед каждым тестом"""
        self.bot = EnhancedFAQBot(data_file=":memory:")  # В памяти, не на диске
    
    def test_bot_initialization(self):
        """Тест инициализации бота"""
        assert self.bot is not None
        assert hasattr(self.bot, 'faq')
        assert isinstance(self.bot.faq, dict)
    
    def test_load_default_data(self):
        """Тест загрузки стандартных данных"""
        assert len(self.bot.faq) > 0
        assert "привет" in self.bot.faq
        assert "как зарегистрироваться" in self.bot.faq
    
    def test_normalize_text(self):
        """Тест нормализации текста"""
        text = "  ПРИВЕТ! Как дела?  "
        normalized = self.bot.normalize_text(text)
        assert normalized == "привет! как дела?"
        assert self.bot.normalize_text("") == ""
    
    def test_find_exact_match(self):
        """Тест точного совпадения"""
        question = "привет"
        match, similarity = self.bot.find_best_match(question)
        assert match == "привет"
        assert similarity == 1.0
    
    def test_get_answer_exact(self):
        """Тест получения ответа при точном совпадении"""
        answer = self.bot.get_answer("привет")
        assert "Здравствуйте" in answer
        assert "VK WorkSpace" in answer
    
    def test_get_answer_no_match(self):
        """Тест когда нет совпадения"""
        answer = self.bot.get_answer("абсолютно неизвестный вопрос")
        assert "не нашел" in answer.lower() or "извините" in answer.lower()

def test_bot_import():
    """Простой тест импорта"""
    import bot
    assert hasattr(bot, 'EnhancedFAQBot')
    assert hasattr(bot, 'main')