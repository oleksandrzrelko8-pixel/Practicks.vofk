import json
import os
import datetime

DATA_FILE = "notes.json"

def load_notes():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Помилка при завантаженні файлу: {e}")
        return []

def save_notes(notes):
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(notes, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Помилка при збереженні файлу: {e}")

def get_next_id(notes):
    if not notes:
        return 1
    return max(note['id'] for note in notes) + 1

def add_note(notes):
    print("\n--- Додавання нової нотатки ---")
    title = input("Введіть заголовок: ").strip()
    if not title:
        print("Заголовок не може бути порожнім!")
        return

    content = input("Введіть текст нотатки: ").strip()
    tags_input = input("Введіть теги (через кому): ").strip()
    
    tags = [tag.strip() for tag in tags_input.split(',')] if tags_input else []
    # Видалення порожніх тегів
    tags = [tag for tag in tags if tag]

    note = {
        "id": get_next_id(notes),
        "title": title,
        "content": content,
        "tags": tags,
        "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    notes.append(note)
    save_notes(notes)
    print(f"Нотатку '{title}' успішно додано!")

def view_all_notes(notes):
    print("\n--- Всі нотатки ---")
    if not notes:
        print("Нотаток поки немає.")
        return
    for note in notes:
        tags_str = ", ".join(note['tags']) if note['tags'] else "немає тегів"
        print(f"[ID: {note['id']}] {note['title']} | Теги: {tags_str}")

def search_notes_by_tag(notes):
    print("\n--- Пошук за тегом ---")
    tag_to_search = input("Введіть тег для пошуку: ").strip()
    if not tag_to_search:
        print("Тег не може бути порожнім!")
        return

    found_notes = [note for note in notes if tag_to_search in note['tags']]
    
    if not found_notes:
        print(f"Нотаток з тегом '{tag_to_search}' не знайдено.")
    else:
        print(f"Знайдено нотаток: {len(found_notes)}")
        for note in found_notes:
            tags_str = ", ".join(note['tags'])
            print(f"[ID: {note['id']}] {note['title']} | Теги: {tags_str}")

def view_note_by_id(notes):
    print("\n--- Перегляд нотатки ---")
    try:
        note_id = int(input("Введіть ID нотатки: ").strip())
    except ValueError:
        print("Помилка: ID має бути числом!")
        return

    for note in notes:
        if note['id'] == note_id:
            print("\n" + "="*30)
            print(f"ID:         {note['id']}")
            print(f"Заголовок:  {note['title']}")
            print(f"Створено:   {note['created_at']}")
            print(f"Теги:       {', '.join(note['tags']) if note['tags'] else 'немає'}")
            print("-" * 30)
            print(note['content'])
            print("="*30)
            return
            
    print(f"Нотатку з ID {note_id} не знайдено.")

def edit_note(notes):
    print("\n--- Редагування нотатки ---")
    try:
        note_id = int(input("Введіть ID нотатки для редагування: ").strip())
    except ValueError:
        print("Помилка: ID має бути числом!")
        return

    for note in notes:
        if note['id'] == note_id:
            print(f"Редагування нотатки: {note['title']}")
            
            new_title = input(f"Новий заголовок (залиште порожнім, щоб не змінювати [{note['title']}]): ").strip()
            if new_title:
                note['title'] = new_title

            new_content = input("Новий текст (залиште порожнім, щоб не змінювати): ").strip()
            if new_content:
                note['content'] = new_content

            current_tags = ", ".join(note['tags'])
            new_tags_input = input(f"Нові теги через кому (залиште порожнім, щоб не змінювати [{current_tags}]): ").strip()
            if new_tags_input:
                tags = [tag.strip() for tag in new_tags_input.split(',')]
                note['tags'] = [tag for tag in tags if tag]
                
            note['updated_at'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            save_notes(notes)
            print("Нотатку успішно оновлено!")
            return

    print(f"Нотатку з ID {note_id} не знайдено.")

def delete_note(notes):
    print("\n--- Видалення нотатки ---")
    try:
        note_id = int(input("Введіть ID нотатки для видалення: ").strip())
    except ValueError:
        print("Помилка: ID має бути числом!")
        return

    for i, note in enumerate(notes):
        if note['id'] == note_id:
            confirm = input(f"Ви впевнені, що хочете видалити нотатку '{note['title']}'? (т/н): ").strip().lower()
            if confirm in ['т', 'y', 'так', 'yes']:
                del notes[i]
                save_notes(notes)
                print("Нотатку видалено!")
            else:
                print("Видалення скасовано.")
            return

    print(f"Нотатку з ID {note_id} не знайдено.")


def main():
    notes = load_notes()
    
    while True:
        print("\n=== НОТАТНИК ІЗ ТЕГАМИ ===")
        print("1. Додати нотатку")
        print("2. Переглянути всі нотатки")
        print("3. Знайти нотатки за тегом")
        print("4. Переглянути нотатку за ID")
        print("5. Редагувати нотатку")
        print("6. Видалити нотатку")
        print("0. Вийти")
        
        choice = input("Оберіть дію (0-6): ").strip()
        
        if choice == '1':
            add_note(notes)
        elif choice == '2':
            view_all_notes(notes)
        elif choice == '3':
            search_notes_by_tag(notes)
        elif choice == '4':
            view_note_by_id(notes)
        elif choice == '5':
            edit_note(notes)
        elif choice == '6':
            delete_note(notes)
        elif choice == '0':
            print("Роботу завершено. До побачення!")
            break
        else:
            print("Некоректний вибір. Будь ласка, введіть число від 0 до 6.")

if __name__ == "__main__":
    main()
