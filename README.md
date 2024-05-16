# Open edX iOS

Modern vision of the mobile application for the Open edX platform from Raccoon Gang.

[Documentation](Documentation/Documentation.md)

## Building
1. Check out the source code:

        git clone https://github.com/openedx/openedx-app-ios.git

2. Navigate to the project folder and run ``pod install``.

3. Open ``OpenEdX.xcworkspace``.

4. Ensure that the ``OpenEdXDev``, ``OpenEdXStage`` or ``OpenEdXProd`` scheme is selected.

5. Configure `config_settings.yaml` inside `default_config` and `config.yaml` inside sub direcroties to point to your OpenEdx configuration [Configuration Documentation](./Documentation/CONFIGURATION_MANAGEMENT.md)

6. Click the **Run** button.

## Translations
### Getting translations for the app.
Translations aren't included in the source code of this repository as of [OEP-58](https://docs.openedx.org/en/latest/developers/concepts/oep58.html). Therefore, it needs to be pulled before testing or publishing to App Store.

To get the latest translations for all languages use the following command:
```bash
	make pull_translations
```
- Run [`atlas pull`](https://github.com/openedx/openedx-atlas) to download the latest translations file from the [openedx/openedx-translations](https://github.com/openedx/openedx-translations) repository which contains the latest translations for all languages.
- The translations will be pulled into a single file `I18N/uk.lproj/Localization.strings` ([example](https://github.com/openedx/openedx-translations/blob/2737aac533c4e6a621fcf6b9c003ac47ec3bcfcb/translations/openedx-app-ios/I18N/uk.lproj/Localizable.strings)).
- The translation file is split into each module e.g. `Discovery/Discovery/uk.lproj/Localization.strings`.
- The `I18N/uk.lproj/Localization.strings` is removed.
   
  After this command is run the application can load the translations by changing the device (or the emulator) language in the settings.

#### Using custom translations
runs , which allows to use custom translations with the following options:

By default, the command `make pull_translations` runs [`atlas pull`](https://github.com/openedx/openedx-atlas) which pulls transaltions from the [openedx-translations repository](https://github.com/openedx/openedx-translations).

You can use custom translations on your fork of the openedx-translations repository by setting the following configuration parameters:

- `--revision` (default: `"main"`): Branch or git tag to pull translations from.
- `--repository` (default: `"openedx/openedx-translations"`). GitHub repository slug. There's a feature request to [support GitLab and other providers](https://github.com/openedx/openedx-atlas/issues/20).

Arguments can be passed via the `ATLAS_OPTIONS` environment variable as shown below:
``` bash
make ATLAS_OPTIONS='--repository=<your-github-org>/<repository-name> --revision=<branch-name>' pull_translations
```
Additional arguments can be passed to `atlas pull`. Refer to the [atlas documentations ](https://github.com/openedx/openedx-atlas) for more information.

#### Testing translations
Until the [pull request #422](https://github.com/openedx/openedx-app-ios/pull/422) is merged, translations needs to be pulled from the testing branch `Zeit-Labs/openedx-translations` repo under `fc_55_sample` branch with the following options:
``` bash
    make ATLAS_OPTIONS='--repository=Zeit-Labs/openedx-translations --revision=fc_55_sample' pull_translations
```
### How to translate the app
	
Translations are managed in the [open-edx/openedx-translations](https://app.transifex.com/open-edx/openedx-translations/dashboard/) Transifex project.

To translate the app join Transifex and add your translations `openedx-app-ios` resource:

 - https://app.transifex.com/open-edx/openedx-translations/openedx-app-ios/ (the link will start working after the [pull request #442](https://github.com/openedx/openedx-app-ios/pull/422) is merged)

Once the resource is both 100% translated and reviewed Transifex will push it to the [openedx-translations](https://github.com/openedx/openedx-translations) repository and developers can use the translations in their app.

By default, all translations are disregarded in this repository except for the English translation.


## API
This project targets on the latest Open edX release and rely on the relevant mobile APIs.

If your platform version is older than December 2023, please follow the instructions to use the [API Plugin](./Documentation/APIs_Compatibility.md).

## License
The code in this repository is licensed under the Apache-2.0 license unless otherwise noted.

Please see [LICENSE](https://github.com/openedx/openedx-app-ios/blob/main/LICENSE) file for details.
