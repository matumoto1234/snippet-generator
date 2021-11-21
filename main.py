import glob
import yaml
import json


def get_directory_paths_from_config() -> list(str):
    try:
        with open('./config.yml', 'r') as file:
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


def get_file_paths(directory_paths) -> list(str):
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


def transform_quote(ch: str) -> str:
    if ch == '"':
        return '\\"'
    if ch == '\\':
        return '\\\\'
    return ch


def transformed_file_datas(file_path: str) -> list(str):
    with open(file_path, 'r') as file:
        datas = []

        lines = file.readlines()

        for line in lines:
            line = ''.join(list(map(transform_quote, line)))
            datas.append(line)

        return datas


def get_file_name(file_path: str) -> str:
    return file_path.split('/')[-1]


def trimming_extention(file_name: str) -> str:
    return file_name.split('.')[0]


def main():
    print('Hello! snippet-generator.')

    directory_paths: list(str) = get_directory_paths_from_config()

    file_paths: list(str) = get_file_paths(directory_paths)

    snippets = []

    for file_path in file_paths:
        file_datas: list(str) = transformed_file_datas(file_path)

        file_name: str = get_file_name(file_path)

        file_name_without_extention: str = trimming_extention(file_name)

        snippet = {
            # ファイルの名前 example. hoge-fuga.hpp
            file_name: {
                # cppをつけた拡張子なしのファイルの名前 example. cpphoge-fuga
                "prefix": "cpp" + file_name_without_extention,
                # body
                "body": file_datas,
                # Template of 拡張子なしのファイルの名前 example. Template of hoge-fuga
                "description": "Template of " + file_name_without_extention,
                # scope example. cpp
                "scope": "cpp"
            },
        }

        snippets.append(snippet)
    # end for

    with open('template.code-snippets.json', 'w') as file:
        file.write(json.dumps(snippets))


main()
