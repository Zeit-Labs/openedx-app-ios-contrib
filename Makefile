clean_translations_temp_directory:
	rm -rf I18N/

create_virtual_env:
	rm -rf .venv
	python3 -m venv .venv
	. .venv/bin/activate && pip install -r i18n_scripts/requirements.txt

pull_translations: clean_translations_temp_directory create_virtual_env
	. .venv/bin/activate && atlas pull $(ATLAS_OPTIONS) translations/openedx-app-ios/I18N:I18N
	. .venv/bin/activate && python i18n_scripts/translation.py --split

extract_translations: clean_translations_temp_directory create_virtual_env
	. .venv/bin/activate && python i18n_scripts/translation.py --combine
