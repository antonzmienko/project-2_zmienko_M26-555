import prompt

COMMAND_EXIT = 'exit'
COMMAND_HELP = 'help'

def help_message():
    print('\n***')
    print(f'{COMMAND_EXIT} - выйти из программы')
    print(f'{COMMAND_HELP} - справочная информация')

def ask_command():
    return prompt.string('Введите команду: ')

def welcome():
    print('Первая попытка запустить проект!')
    print()
    help_message()

    while True:
        input  = ask_command()

        if input == COMMAND_EXIT:
            exit()
        elif input == COMMAND_HELP:
            help_message()
        else:
            print('\nНеизвестная команда')