import main

def run_tests():
    # Тестова база
    test_notes = [
        {"id": 1, "title": "Рецепт", "content": "Вода і сіль", "tags": ["кулінарія"]},
        {"id": 2, "title": "Ідеї", "content": "Вивчити Python", "tags": ["навчання", "it"]}
    ]
    
    # Тест 1: Перевірка генерації наступного ID
    next_id = main.get_next_id(test_notes)
    assert next_id == 3, f"Очікувалось 3, отримано {next_id}"
    print("✓ Тест 1 (Генерація ID): пройдено успішно.")

    # Тест 2: Пошук по існуючому тегу
    search_query = "it"
    found = [n for n in test_notes if any(search_query in tag.lower() for tag in n['tags'])]
    assert len(found) == 1, "Помилка пошуку за тегом"
    assert found[0]['id'] == 2, "Знайдено неправильну нотатку"
    print("✓ Тест 2 (Пошук за тегом): пройдено успішно.")

if __name__ == "__main__":
    run_tests()
    print("Всі автотести завершено!")