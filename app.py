"""A minimal MongoDB-powered contact book CLI."""
import os
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from dotenv import load_dotenv


def get_collection():
    load_dotenv()
    uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
    client = MongoClient(uri, serverSelectionTimeoutMS=5000)
    client.admin.command('ping')
    return client, client['contact_book']['contacts']


def add_contact(collection):
    name = input('Name: ').strip()
    email = input('Email: ').strip()
    city = input('City: ').strip()
    if not name or not email:
        print('Name and email are required.')
        return
    if collection.find_one({'email': email}):
        print('A contact with this email already exists.')
        return
    collection.insert_one({'name': name, 'email': email, 'city': city})
    print('Contact added.')


def show_contacts(collection, query=None):
    contacts = collection.find(query or {}, {'_id': 0}).sort('name', 1)
    found = False
    for contact in contacts:
        found = True
        print(f"{contact['name']} | {contact['email']} | {contact.get('city', '')}")
    if not found:
        print('No contacts found.')


def search_contacts(collection):
    term = input('Name to search: ').strip()
    if not term:
        print('Enter a name.')
        return
    # Regex-escape user input to treat it as literal text.
    import re
    show_contacts(collection, {'name': {'$regex': re.escape(term), '$options': 'i'}})


def update_contact(collection):
    email = input('Email of contact to update: ').strip()
    contact = collection.find_one({'email': email})
    if not contact:
        print('Contact not found.')
        return
    name = input(f"New name [{contact['name']}]: ").strip()
    city = input(f"New city [{contact.get('city', '')}]: ").strip()
    changes = {}
    if name:
        changes['name'] = name
    if city:
        changes['city'] = city
    if changes:
        collection.update_one({'_id': contact['_id']}, {'$set': changes})
    print('Contact updated.')


def delete_contact(collection):
    email = input('Email of contact to delete: ').strip()
    result = collection.delete_one({'email': email})
    print('Contact deleted.' if result.deleted_count else 'Contact not found.')


def main():
    client = None
    try:
        client, collection = get_collection()
        while True:
            print('\n=== Contact Book ===')
            print('1. Add contact\n2. View contacts\n3. Search by name\n4. Update contact\n5. Delete contact\n0. Exit')
            choice = input('Choose an option: ').strip()
            actions = {'1': add_contact, '2': show_contacts, '3': search_contacts,
                       '4': update_contact, '5': delete_contact}
            if choice == '0':
                print('Goodbye!')
                break
            if choice not in actions:
                print('Invalid option.')
                continue
            try:
                actions[choice](collection)
            except PyMongoError as exc:
                print(f'Database operation failed: {exc}')
    except PyMongoError as exc:
        print(f'Cannot connect to MongoDB: {exc}')
        print('Check MONGODB_URI in .env and make sure MongoDB is running.')
    except (KeyboardInterrupt, EOFError):
        print('\nGoodbye!')
    finally:
        if client is not None:
            client.close()


if __name__ == '__main__':
    main()
