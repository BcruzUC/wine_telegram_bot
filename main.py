import pickle as pk
import re

def extract_categories(text):
    all_results = []
    sections = text.strip().split('\n\n')
    # print(sections)

    for section in sections:
        categories = {}
        lines = section.strip().split('\n')
        current_category = None

        for line in lines:
            if ":" in line:
                category, content = re.split(r'\s*:\s*', line, maxsplit=1)
                category = category.lower()
                categories[category] = content.strip().lower()
                current_category = category
            elif current_category:
                categories[current_category] += ' ' + line.strip()

        all_results.append(categories)

    return all_results

def search_wine(wine_list, attribute, attribute_name):
    wines_found = []
    attribute = attribute.lower()
    attribute_name = attribute_name.lower()
    for wine in wine_list:
        if attribute_name in wine[attribute]:
            wines_found.append(wine)
    return wines_found

def print_result(result_list):
    for result in result_list:
        print(f"{result['name']}\nType: {result['type']}\n")

if __name__ == '__main__':
    with open('wines.txt', 'r') as text:
        wine_list = extract_categories(text.read())
    # print(wine_list)
    kinross_wine = search_wine(wine_list, attribute='notes', attribute_name='cherry')
    print_result(kinross_wine)
