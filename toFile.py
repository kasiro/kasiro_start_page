import re
from sys import exit
from pyquery import PyQuery as pq

def normalize_css_indentation(content):
    # Удаляем все существующие отступы
    content = re.sub(r'^[ \t]+', '', content, flags=re.MULTILINE)
    
    # Обрабатываем вложенность
    indent_level = 0
    result = []
    for line in content.splitlines():
        line = line.strip()
        if not line:
            result.append('')
            continue
            
        # Уменьшаем уровень перед закрывающей скобкой
        if line.startswith('}'):
            indent_level = max(0, indent_level - 1)
        
        # Добавляем отступы
        indented_line = (' ' * 4 * indent_level) + line
        result.append(indented_line)
        
        # Увеличиваем уровень после открывающей скобки
        if line.endswith('{'):
            indent_level += 1
    
    # Собираем результат с правильными отступами
    normalized_content = '\n'.join(result)
    
    # Чистим лишние пустые строки
    normalized_content = re.sub(r'\n{3,}', '\n\n', normalized_content)
    
    return normalized_content


def insert_jsx_into_html(output_file, html_file):
    # Читаем HTML файл
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    
    # Находим и заменяем блок script.text в HTML
    doc = pq(html_content)
    text = str(doc('style[type="text/tailwindcss"]').html())
    
    # Сохраняем обновленный HTML
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(
            normalize_css_indentation(
                text.strip()
            )
        )

# Пример использования
insert_jsx_into_html('tailwindcss.css', 'index.html')
