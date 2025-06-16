import random

def process_roll(args):
    if not args:
        return f"🎲 Результат: {random.randint(1, 100)}"

    elif len(args) == 1:
        try:
            limit = int(args[0])
            if limit <= 0:
                raise ValueError("Число должно быть больше 0")
            return f"🎲 От 1 до {limit}: {random.randint(1, limit)}"
        except ValueError:
            return "❌ Введите корректное число или список вариантов"

    else:
        choice = random.choice(args)
        return f"🎲 Выбираю из вариантов: {choice}"