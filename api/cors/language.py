class ManageLanguage():
    def __init__(self, language, word) -> None:
        self.language = language
        self.word = word
        self.default_language = 'en'

    def manage_language(self):
        language_list_data = [{
            'fr': "Bonjour",
            'en': "Good morning"
        }, {
            'fr': "Langue ajoutée avec succès.",
            'en': "Language added with success."
        }]

        for language in language_list_data:
            if self.language == self.default_language:
                return self.word
            else:
                if self.word in language['en']:
                    return language[self.language]
