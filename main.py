# coding: utf-8
from typing import List
import codecs
import glob
import yaml
import json


def get_directory_paths_from_config(config_path: str) -> List[str]:
    try:
        with codecs.open(config_path, 'r', 'utf-8') as file:
            config = yaml.safe_load(file)

            if not config:
                return []

            return config['paths']
    except OSError as err:
        print('Can not open config.yml.')
        print(err)
    except KeyError as err:
        print('Does not decleared \'paths\' in config file')
        print(err)
    except TypeError as err:
        print('TypeError!?')
        print(err)

    return []


def trimming_back_slash(directory_path: str) -> str:
    if directory_path[-1] == '/':
        return directory_path[:-1]
    return directory_path


def get_file_paths(directory_paths) -> List[str]:
    if not directory_paths:
        print('Paths are empty or error!')
        exit(1)

    directory_paths = list(map(trimming_back_slash, directory_paths))

    all_file_paths = []

    for directory_path in directory_paths:
        file_paths = glob.glob(directory_path + '/**', recursive=True)

        # remove self path. example. '/home/octocat/library/data-structure'
        file_paths = file_paths[1:]

        for file_path in file_paths:
            all_file_paths.append(file_path)

    return all_file_paths


def get_exclude_lines(config_path: str) -> List[str]:
    with codecs.open(config_path, 'r', 'utf-8') as file:
        config = yaml.safe_load(file)
        return config['excludeLines']


def transformed_file_datas(file_path: str, exclude_lines: List[str]) -> List[str]:
    extention = file_path.split('.')[-1]
    if extention == 'out' or extention == 'exe':
        return []

    with codecs.open(file_path, 'r', 'utf-8') as file:
        print(file_path + ' is opened')

        datas = []

        lines = file.readlines()

        for line in lines:

            is_exclude = False
            for exclude_line in exclude_lines:
                if exclude_line in line:
                    is_exclude = True

            if(is_exclude):
                continue

            if line[-1] == '\n':
                line = line[:-1]

            datas.append(line)

        return datas


def get_file_name(file_path: str) -> str:
    return file_path.split('/')[-1]


def trimming_extention(file_name: str) -> str:
    return file_name.split('.')[0]


def main():
    print('Hello! snippet-generator.')

    config_path = './config.yml'

    directory_paths: List[str] = get_directory_paths_from_config(config_path)

    file_paths: List[str] = get_file_paths(directory_paths)

    exclude_lines: List[str] = get_exclude_lines(config_path)

    snippets = {}

    for file_path in file_paths:
        file_datas: List[str] = transformed_file_datas(
            file_path, exclude_lines)

        file_name: str = get_file_name(file_path)

        file_name_without_extention: str = trimming_extention(file_name)

        snippet = {
            # cppをつけた拡張子なしのファイルの名前 example. cpphoge-fuga
            "prefix": "cpp" + file_name_without_extention,
            # body
            "body": file_datas,
            # Template of 拡張子なしのファイルの名前 example. Template of hoge-fuga
            "description": "Template of " + file_name_without_extention,
            # scope example. cpp
            "scope": "cpp"
        }

        snippets[file_name] = snippet
    # end for

    with codecs.open('template.code-snippets.json', 'w', 'utf-8') as file:
        file.write(json.dumps(snippets))


main()
