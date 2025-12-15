# src/bot.py
import difflib
import json
import os
from datetime import datetime
import sys

class EnhancedFAQBot:
    def __init__(self, faq_dict=None, data_file=None):
        # Используем переменную окружения или значение по умолчанию
        self.data_file = data_file or os.getenv("DATA_FILE", "faq_data.json")
        
        # Создаем полный путь к файлу данных
        if not os.path.isabs(self.data_file):
            self.data_file = os.path.join(os.getcwd(), self.data_file)
        
        print(f" Файл данных: {self.data_file}")
        print(f" Текущая директория: {os.getcwd()}")
        print(f" Пользователь: {os.getenv('USER', 'docker-user')}")
        
        if faq_dict:
            self.faq = faq_dict
        else:
            self.faq = self.load_data()
        
        self.questions = list(self.faq.keys())
        self.conversation_history = []
    
    def load_data(self):
        """Загружает FAQ из файла, если он существует"""
        print(f" Загрузка данных из: {self.data_file}")
        
        # Создаем директорию если не существует
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    print(f" Данные загружены ({len(data)} вопросов)")
                    return data
            except Exception as e:
                print(f" Ошибка загрузки файла: {e}")
                print(" Использую стандартные данные")
        else:
            print(" Файл не найден, создаю стандартные данные")
        
        # Возвращаем стандартные данные если файла нет
        default_data = {
            "привет": "Здравствуйте! Я — виртуальный помощник VK WorkSpace. Чем могу помочь?",
            "что такое ваш продукт": "Наш продукт - это платформа для эффективного общения и управления задачами в компании.",
            "как зарегистрироваться": "Для регистрации перейдите на сайт и следуйте инструкциям.",
            "как я могу изменить свой пароль": "Для изменения пароля перейдите в настройки аккаунта и выберите пункт 'Изменить пароль'.",
            "как связаться с поддержкой": "Вы можете связаться с нашей службой поддержки через email: vkteamssupport@mail.ru.",
            "что делать если я забыл пароль": "Если вы забыли пароль, воспользуйтесь функцией восстановления пароля на странице входа."
        }
        
        # Сохраняем стандартные данные
        self.save_data(default_data)
        return default_data
    
    def save_data(self, data=None):
        """Сохраняет FAQ в файл"""
        try:
            data_to_save = data or self.faq
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data_to_save, f, ensure_ascii=False, indent=2)
            print(f" Данные сохранены в {self.data_file}")
            return True
        except Exception as e:
            print(f" Ошибка сохранения: {e}")
            return False
    
    def find_best_match(self, user_question, threshold=0.5):
        """Находит наиболее похожий вопрос в базе данных"""
        user_question = self.normalize_text(user_question)
        
        # Ищем точное совпадение
        if user_question in self.faq:
            return user_question, 1.0
        
        # Ищем похожие вопросы
        matches = difflib.get_close_matches(
            user_question, 
            self.questions, 
            n=3,
            cutoff=threshold
        )
        
        if matches:
            best_match = matches[0]
            best_similarity = difflib.SequenceMatcher(None, user_question, best_match).ratio()
            
            for match in matches[1:]:
                similarity = difflib.SequenceMatcher(None, user_question, match).ratio()
                if similarity > best_similarity:
                    best_match = match
                    best_similarity = similarity
            
            return best_match, best_similarity
        
        return None, 0
    
    def normalize_text(self, text):
        """Нормализует текст для сравнения"""
        text = text.lower().strip()
        words = text.split()
        return ' '.join(words)
    
    def get_suggestions(self, user_question):
        """Получает предложения похожих вопросов"""
        user_question = self.normalize_text(user_question)
        suggestions = difflib.get_close_matches(
            user_question, 
            self.questions, 
            n=3,
            cutoff=0.3
        )
        return suggestions
    
    def get_answer(self, user_question):
        """Получает ответ на вопрос пользователя"""
        match, similarity = self.find_best_match(user_question)
        
        self.conversation_history.append({
            'question': user_question,
            'match': match,
            'similarity': similarity,
            'timestamp': datetime.now().isoformat()
        })
        
        if match:
            answer = self.faq[match]
            if similarity < 0.8:
                suggestions = self.get_suggestions(user_question)
                suggestion_text = ""
                if len(suggestions) > 1:
                    suggestion_text = "\n\nВозможно, вы имели в виду:\n"
                    for i, suggestion in enumerate(suggestions[:3], 1):
                        suggestion_text += f"{i}. {suggestion}\n"
                
                return f"Возможно, вы спрашиваете: '{match}'?\n\n{answer}{suggestion_text}"
            else:
                return answer
        else:
            suggestions = self.get_suggestions(user_question)
            if suggestions:
                suggestion_text = "\nВозможно, вы хотите спросить о:\n"
                for i, suggestion in enumerate(suggestions, 1):
                    suggestion_text += f"{i}. {suggestion}\n"
                return f"Извините, я не нашел точного ответа.{suggestion_text}"
            else:
                return "Извините, я не нашел ответ на ваш вопрос. Можете переформулировать его или обратиться в поддержку."
    
    def show_all_topics(self):
        """Показывает все доступные темы"""
        print("\n" + "=" * 60)
        print(" ДОСТУПНЫЕ ТЕМЫ:")
        print("=" * 60)
        for i, question in enumerate(self.questions, 1):
            print(f"{i}. {question}")
        print("=" * 60)
    
    def add_question(self, question, answer):
        """Добавляет новый вопрос в базу"""
        normalized_q = self.normalize_text(question)
        self.faq[normalized_q] = answer
        self.questions = list(self.faq.keys())
        if self.save_data():
            print(f" Вопрос добавлен: '{normalized_q}'")
        else:
            print(f" Не удалось сохранить вопрос")
    
    def show_history(self):
        """Показывает историю диалога"""
        if not self.conversation_history:
            print("\n📜 История пуста")
            return
        
        print("\n" + "=" * 60)
        print(" ИСТОРИЯ ДИАЛОГА:")
        print("=" * 60)
        for i, item in enumerate(self.conversation_history[-10:], 1):
            time_str = datetime.fromisoformat(item['timestamp']).strftime("%H:%M:%S")
            print(f"\n[{time_str}]  Вы: {item['question'][:50]}{'...' if len(item['question']) > 50 else ''}")
            if item['match']:
                print(f"    Сопоставление: '{item['match']}' ({item['similarity']:.1%})")
        print("=" * 60)
    
    def run(self):
        """Запускает интерактивный режим бота"""
        bot_name = os.getenv("BOT_NAME", "VK WorkSpace FAQ Bot")
        
        print("=" * 60)
        print(f" {bot_name}")
        print("=" * 60)
        print("\n Команды:")
        print("  'темы'    - показать все доступные вопросы")
        print("  'добавить' - добавить новый вопрос")
        print("  'история' - показать историю диалога")
        print("  'сохранить' - принудительно сохранить данные")
        print("  'выход'   - завершить работу")
        print("-" * 60)
        print(f" Данные сохраняются в: {self.data_file}")
        print("-" * 60)
        
        while True:
            try:
                user_input = input("\n👤 Вы: ").strip()
                
                # Обработка команд
                if user_input.lower() in ['выход', 'exit', 'quit', 'стоп']:
                    print("\n Бот: До свидания! Буду рад помочь вам снова!")
                    print(" Сохранение данных...")
                    self.save_data()
                    break
                
                elif user_input.lower() == 'темы':
                    self.show_all_topics()
                    continue
                
                elif user_input.lower() == 'история':
                    self.show_history()
                    continue
                
                elif user_input.lower() == 'сохранить':
                    if self.save_data():
                        print(" Бот: Данные успешно сохранены!")
                    else:
                        print(" Бот: Не удалось сохранить данные")
                    continue
                
                elif user_input.lower() == 'добавить':
                    print("\n Добавление нового вопроса:")
                    new_q = input(" Вопрос: ").strip()
                    new_a = input(" Ответ: ").strip()
                    if new_q and new_a:
                        self.add_question(new_q, new_a)
                    else:
                        print(" Вопрос и ответ не могут быть пустыми")
                    continue
                
                if not user_input:
                    print(" Бот: Пожалуйста, задайте ваш вопрос.")
                    continue
                
                answer = self.get_answer(user_input)
                print(f"\n Бот: {answer}")
                
            except KeyboardInterrupt:
                print("\n\n Бот: Работа прервана пользователем.")
                self.save_data()
                break
            except EOFError:
                print("\n\n Бот: Конец ввода.")
                self.save_data()
                break
            except Exception as e:
                print(f"\n Бот: Произошла ошибка: {e}")

def main():
    print(" Запуск FAQ бота...")
    
    # Получаем путь к файлу данных из переменных окружения
    data_file = os.getenv("DATA_FILE")
    
    # Создаем и запускаем бота
    bot = EnhancedFAQBot(data_file=data_file)
    bot.run()

if __name__ == "__main__":
    main()