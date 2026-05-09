from services.birthday import (
    get_upcoming_birthdays,
    build_collection_data
)

birthdays = get_upcoming_birthdays()

print("Найближчі ДН:")
print()

for birthday_user in birthdays:
    collection = build_collection_data(birthday_user)

    print(f"Іменинник: {birthday_user['ПІБ']}")
    print(f"Сума: {collection['amount']} грн")
    print(f"Учасників: {len(collection['participants'])}")

    print()

    for user in collection["participants"]:
        print(user["ПІБ"])

    print("-" * 30)