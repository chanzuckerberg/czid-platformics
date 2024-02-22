class SettingsSingleton:
    settings_obj = None

    # Call SettingsSingleton.get() to get the settings obj for the current execution environment.
    @classmethod
    def get(cls):
        if not cls.settings_obj:
            raise Exception("Settings not defined in this environment")
        return cls.settings_obj

    @classmethod
    def set(cls, obj):
        cls.settings_obj = obj
