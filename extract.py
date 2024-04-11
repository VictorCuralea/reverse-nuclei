import os
import sys
import yaml
import csv

def parse_yaml(file_path, csv_writer):
    with open(file_path, 'r') as file:
        content = yaml.safe_load(file)
        if 'http' in content:
            for http_block in content['http']:
                if 'matchers' in http_block:
                    for matcher in http_block['matchers']:
                        words_or_regex = matcher.get('words') or matcher.get('regex') or []
                        if not isinstance(words_or_regex, list):
                            words_or_regex = [words_or_regex]
                        for word_or_regex in words_or_regex:
                            method = http_block.get('method', '')
                            paths = http_block.get('path', [''])
                            for path in paths:
                                csv_writer.writerow([file_path, method, path, matcher.get('part', ''), matcher['type'], word_or_regex])

def traverse_dir(root_dir, csv_writer):
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.yaml') or file.endswith('.yml'):
                parse_yaml(os.path.join(root, file), csv_writer)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <directory_path>")
    else:
        directory_path = sys.argv[1]
        with open('output.csv', 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
            csv_writer.writerow(['File', 'Method', 'Path', 'Part', 'Type', 'WordOrRegex'])
            traverse_dir(directory_path, csv_writer)
