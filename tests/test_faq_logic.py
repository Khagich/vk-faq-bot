# tests/test_faq_logic.py
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from bot import EnhancedFAQBot

def test_add_new_question():
    """Тест добавления нового вопроса"""
    bot = EnhancedFAQBot(faq_dict={"тест": "ответ"})
    initial_count = len(bot.faq)
    
    bot.add_question("новый вопрос", "новый ответ")
    
    assert len(bot.faq) == initial_count + 1
    assert "новый вопрос" in bot.faq
    assert bot.faq["новый вопрос"] == "новый ответ"

def test_similarity_matching():
    """Тест нечеткого поиска"""
    bot = EnhancedFAQBot(faq_dict={
        "как изменить пароль": "Идите в настройки",
        "регистрация": "На сайте"
    })
    
    # Похожий вопрос
    match, similarity = bot.find_best_match("как поменять пароль", threshold=0.4)
    assert match is not None
    assert similarity > 0.4

def test_empty_question():
    """Тест пустого вопроса"""
    bot = EnhancedFAQBot()
    answer = bot.get_answer("")
    assert "пожалуйста" in answer.lower() or "вопрос" in answer.lower()