clean_translations_temp_directory:
	rm -rf I18N/

translation_requirements:
	pip install -r i18n_scripts/requirements.txt

pull_translations: clean_translations_temp_directory
	atlas pull $(ATLAS_OPTIONS) translations/openedx-app-ios/I18N:I18N
	python i18n_scripts/translation.py --split

extract_translations: clean_translations_temp_directory
	python i18n_scripts/translation.py --combine
