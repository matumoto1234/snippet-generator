# coding: utf-8
import os
import glob
import yaml
import json
import codecs
import subprocess

from typing import List
from subprocess import PIPE


def get_library_paths_from(config_path: str) -> List[str]:
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

        file_paths = list(map(trimming_back_slash, file_paths))
        file_paths = list(filter(os.path.isfile, file_paths))

        for file_path in file_paths:
            all_file_paths.append(file_path)

    return all_file_paths


def get_exclude_lines(config_path: str) -> List[str]:
    with codecs.open(config_path, 'r', 'utf-8') as file:
        config = yaml.safe_load(file)
        return config['excludeLines']


def get_prefix_name_case(config_path: str) -> str:
    with codecs.open(config_path, 'r', 'utf-8') as file:
        config = yaml.safe_load(file)
        prefix_name_case = config['prefixNameCase']
        assert prefix_name_case == 'Snake' or prefix_name_case == 'Camel' or prefix_name_case == 'Pascal' or prefix_name_case == 'Kebab'
        return prefix_name_case


def get_use_oj_bundle(config_path: str) -> True:
    with codecs.open(config_path, 'r', 'utf-8') as file:
        config = yaml.safe_load(file)
        use_oj_bundle = config['useOjBundle']
        assert use_oj_bundle == True or use_oj_bundle == False
        return use_oj_bundle


def transformed_file_datas(file_path: str, exclude_lines: List[str], use_oj_bundle) -> List[str]:
    extention = file_path.split('.')[-1]
    if extention == 'out' or extention == 'exe':
        return []

    if use_oj_bundle:
        args = ['oj-bundle', file_path]

        try:
            res = subprocess.run(args, stdout=PIPE, stderr=PIPE, text=True)
        except:
            print('Failed file open : ' + file_path)
            exit(1)

        print('Success file open : ' + file_path)
        datas = []

        if res.stdout:
            lines = res.stdout.splitlines()

            is_empty_line_continuous_from_the_beginning = True

            for line in lines:
                if '#line' in line:
                    continue

                is_exclude = False
                for exclude_line in exclude_lines:
                    if exclude_line in line:
                        is_exclude = True

                if is_exclude:
                    continue

                if line != '':
                    is_empty_line_continuous_from_the_beginning = False

                if is_empty_line_continuous_from_the_beginning:
                    continue

                datas.append(line)

        return datas
    # end if use_oj_bundle

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


def to_upper_only_first(s: str) -> str:
    if not s:
        return ''
    return s[0].upper() + s[1:]


def transform_name_case(file_name_without_extention: str, prefix_name_case: str) -> str:
    if prefix_name_case == 'Snake':
        return '_'.join(file_name_without_extention.split('-'))
    elif prefix_name_case == 'Kebab':
        return file_name_without_extention
    elif prefix_name_case == 'Pascal':
        words = file_name_without_extention.split('-')
        words = list(map(to_upper_only_first, words))
        return ''.join(words)
    elif prefix_name_case == 'Camel':
        words = file_name_without_extention.split('-')
        words = list(map(to_upper_only_first, words))
        file_name_without_extention = ''.join(words)
        return file_name_without_extention[0].lower()
    else:
        print('The prefixNameCase is error. Please check your config.yml')
        exit(1)


def main():
    print('Hello! snippet-generator.')

    config_path = './config.yml'

    directory_paths: List[str] = get_library_paths_from(config_path)

    file_paths: List[str] = get_file_paths(directory_paths)

    exclude_lines: List[str] = get_exclude_lines(config_path)

    prefix_name_case: str = get_prefix_name_case(config_path)

    use_oj_bundle = get_use_oj_bundle(config_path)

    snippets = {}

    for file_path in file_paths:
        file_datas: List[str] = transformed_file_datas(
            file_path, exclude_lines, use_oj_bundle)

        file_name: str = get_file_name(file_path)

        file_name_without_extention: str = trimming_extention(file_name)

        file_name_without_extention: str = transform_name_case(
            file_name_without_extention, prefix_name_case)

        snippet = {
            # cppをつけた拡張子なしのファイルの名前 example. cpphoge-fuga
            'prefix': 'cpp' + file_name_without_extention,
            # body
            'body': file_datas,
            # Template of 拡張子なしのファイルの名前 example. Template of hoge-fuga
            'description': 'Template of ' + file_name_without_extention,
            # scope example. cpp
            'scope': 'cpp'
        }

        snippets[file_name] = snippet
    # end for

    with codecs.open('template.code-snippets.json', 'w', 'utf-8') as file:
        json.dump(snippets, file, indent=2, ensure_ascii=False)


main()
