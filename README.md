# ITMO Abiturient Bachelor Parser

Скрипт, при помощи которого Вы можете получить .xlsx таблицу со всеми подавшими абитуриентами на бакалавриат ИТМО и увидеть их баллы ВИ (ЕГЭ)

## Использование
Клонируем репозиторий, переходим в его каталог, устанавливаем необходимые пакеты при помощи `pip`, запускаем `main.py` и ждем окончания работы скрипта. Все данные будут сохранены в файл `itmo_abiturients.xlsx`

```bash
git clone https://github.com/krpff/itmo-abit-parser.git
cd itmo-abit-parser
pip install requests xlsxwriter random_user_agent
python main.py
```



