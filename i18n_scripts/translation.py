#!/usr/bin/env python3
"""
This script contains the necessary methods to accomplish two functions:
 1- Combine the English translations from all modules in the repository to the I18N directory. After the English
    translation is combined, it will be pushed to the openedx-translations repository as described in OEP-58.
 2- Split all other Languages. After pulling the translations from the openedx-translations repository via atlas pull,
    there will be a single strings file for each language, the "split_translation_files" method will run through each
    language file in the I18N directory and split it into the modules.
"""

import argparse
import os
from collections import OrderedDict, defaultdict
import localizable


def parse_arguments():
    """
    This function is the argument parser for this script.
    The script takes only one of the two arguments --split or --combine as indicated below.
    """
    parser = argparse.ArgumentParser(description='Split or combine translations.')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--split', action='store_true',
                       help='Split translations into separate files for each module and language.')
    group.add_argument('--combine', action='store_true',
                       help='Combine the English translations from all modules into a single file.')
    return parser.parse_args()


def get_translation_file_path(modules_dir, module_name, lang_dir, create_dirs=False):
    """
    Retrieves the path of the translation file from the module name

    Parameters:
        modules_dir (str): The path to the directory containing all the modules.
        module_name (str): The module's name that we want.
        lang_dir (str): The language directory's name that we want.
        create_dirs (bool): If True it will create the parent directories when they do not exist, default to False.

    Returns:
        file_path (str): The module's translation path.
    """
    lang_dir_path = os.path.join(modules_dir, module_name, module_name, lang_dir)
    if create_dirs:
        os.makedirs(lang_dir_path, exist_ok=True)
    translation_file = os.path.join(lang_dir_path, 'Localizable.strings')
    return translation_file


def get_modules_to_translate(modules_dir):
    """
    Retrieve the names of modules that have translation files for a specified language.

    Parameters:
        modules_dir (str): The path to the directory containing all the modules.

    Returns:
        list of str: A list of module names that have translation files for the specified language.
    """
    modules_list = [
        directory for directory in os.listdir(modules_dir)
        if (
            os.path.isdir(os.path.join(modules_dir, directory))
            and os.path.isfile(get_translation_file_path(modules_dir, directory, 'en.lproj'))
            and directory != 'I18N'
        )
    ]
    return modules_list


def get_translations(modules_dir):
    """
    Retrieve the translations from all specified modules as OrderedDict.

    Parameters:
        modules_dir (str): The directory containing the modules.

    Returns:
        OrderedDict of dict: An ordered dict of dictionaries containing the 'key', 'value', and 'comment' for each
        translation line. The key of the outer OrderedDict consists of the value of the translation key combined with
        the name of the module containing the translation.
    """
    translations = []
    modules = get_modules_to_translate(modules_dir)
    for module in modules:
        translation_file = get_translation_file_path(modules_dir, module, lang_dir='en.lproj')
        module_translation = localizable.parse_strings(filename=translation_file)

        translations += [
            {
                'key': f"{module}.{translation_entry['key']}",
                'value': translation_entry['value'],
                'comment': translation_entry['comment']
            } for translation_entry in module_translation
        ]

    return {'I18N': translations}

#
# def write_combined_translation_file(modules_dir, content_ordered_dict):
#     """
#     Write the contents of an ordered dictionary to a Localizable.strings file.
#
#     This function takes an ordered dictionary containing translation data and writes it to a Localizable.strings
#     file located in the 'I18N/en.lproj' directory within the specified modules directory. It creates the directory
#     if it doesn't exist.
#
#     Parameters:
#        modules_dir (str): The path to the modules directory
#        where the I18N directory will be written.
#        content_ordered_dict (OrderedDict): An ordered dictionary containing translation data. The keys
#        are the translation keys, and the values are dictionaries with 'value' and 'comment' keys representing the
#        translation value and optional comments, respectively.
#     """
#     translation_file_path = get_translation_file_path(modules_dir, 'I18N', 'en.lproj', create_dirs=True)
#     with open(translation_file_path, 'w') as f:
#         for key, value in content_ordered_dict.items():
#             write_line_and_comment(f, value, key=key)


def combine_translation_files(modules_dir=None):
    """
    Combine translation files from different modules into a single file.
    """
    if not modules_dir:
        modules_dir = os.path.dirname(os.path.dirname(__file__))
    combined_translation_dict = get_translations(modules_dir)
    write_translations_to_modules(modules_dir, 'en.lproj', combined_translation_dict)

    # write_combined_translation_file(modules_dir, combined_translation_dict)


def get_languages_dirs(modules_dir):
    """
    Retrieve directories containing language files for translation.

    Args:
        modules_dir (str): The directory containing all the modules.

    Returns:
        list: A list of directories containing language files for translation. Each directory represents
              a specific language and ends with the '.lproj' extension.

    Example:
        Input:
            get_languages_dirs('/path/to/modules')
        Output:
            ['ar.lproj', 'uk.lproj', ...]
    """
    lang_parent_dir = os.path.join(modules_dir, 'I18N', 'I18N')
    languages_dirs = [
        directory for directory in os.listdir(lang_parent_dir)
        if directory.endswith('.lproj') and directory != "en.lproj"
    ]
    return languages_dirs


def extract_translations_from_file(modules_dir, lang_dir):
    """
    Separate translations from a translation file into modules.

    Args:
        modules_dir (str): The directory containing all the modules.
        lang_dir (str): The directory containing the translation file being split.

    Returns:
        dict: A dictionary containing translations split by module. The keys are module names,
              and the values are lists of dictionaries, each containing the 'key', 'value', and 'comment'
              for each translation entry within the module.

    Example:
        Input:
            separate_translation_to_modules('/path/to/modules', 'uk.lproj')
        Output:
            {
                'module1': [
                    {'key': 'translation_key', 'value': 'translation_value', 'comment': 'translation_comment'},
                    ...
                ],
                'module2': [
                    ...
                ],
                ...
            }
    """
    translations = defaultdict(list)
    translations_file_path = get_translation_file_path(modules_dir, 'I18N', lang_dir)
    lang_list = localizable.parse_strings(filename=translations_file_path)
    for translation_entry in lang_list:
        module_name, key_remainder = translation_entry['key'].split('.', maxsplit=1)
        split_entry = {
            'key': key_remainder,
            'value': translation_entry['value'],
            'comment': translation_entry['comment']
        }
        translations[module_name].append(split_entry)
    return translations


def write_translations_to_modules(modules_dir, lang_dir, modules_translations):
    """
    Write translations to language files for each module.

    Args:
        modules_dir (str): The directory containing all the modules.
        lang_dir (str): The directory of the translation file being written.
        modules_translations (dict): A dictionary containing translations for each module.

    Returns:
        None
    """
    for module, translation_list in modules_translations.items():
        translation_file_path = get_translation_file_path(modules_dir, module, lang_dir, create_dirs=True)
        with open(translation_file_path, 'w') as f:
            for translation_entry in translation_list:
                write_line_and_comment(f, translation_entry)


def _escape(s):
    """
    Reverse the replacements performed by _unescape() in the localizable library
    """
    s = s.replace('\n', r'\n').replace('\r', r'\r').replace('"', r'\"')
    return s


def write_line_and_comment(file, entry, key=None):
    """
    Write a translation line with an optional comment to a file.

    Args:
        file (file object): The file object to write to.
        entry (dict): A dictionary containing the translation entry with 'key', 'value', and optional 'comment'.
        key (str, optional): The key to use in the translation line. If not provided, 'entry["key"]' is used.

    Returns:
        None
    """
    comment = entry.get('comment')  # Retrieve the comment, if present
    key = key if key else entry['key']
    if comment:
        file.write(f"/* {comment} */\n")
    file.write(f'"{key}" = "{_escape(entry["value"])}";\n')


def split_translation_files(modules_dir=None):
    """
    Split translation files into separate files for each module and language.

    Args:
        modules_dir (str, optional): The directory containing all the modules. If not provided,
            it defaults to the parent directory of the directory containing this script.

    Returns:
        None

    Example:
        split_translation_files('/path/to/modules')
    """
    if not modules_dir:
        modules_dir = os.path.dirname(os.path.dirname(__file__))
    languages_dirs = get_languages_dirs(modules_dir)
    for lang_dir in languages_dirs:
        translations = extract_translations_from_file(modules_dir, lang_dir)
        write_translations_to_modules(modules_dir, lang_dir, translations)


def main():
    args = parse_arguments()
    if args.split:
        # Call the function to split translations
        split_translation_files()
    elif args.combine:
        # Call the function to combine translations
        combine_translation_files()


if __name__ == "__main__":
    main()
