from faker import Faker

fake = Faker()


class MakeFactory:
    def __init__(self, factory, session, **kwargs):
        self.Factory = factory
        self.session = session
        self.kwargs = kwargs

    def _set_session(self):
        self.Factory._meta.sqlalchemy_session = self.session

    @staticmethod
    def modify_fields(form, exclude: set | None):
        """Removes fields from a form."""
        if exclude is None:
            exclude = set()  # Initialize a new set

        fields_to_remove = {'id', 'created_at', 'updated_at',
                            'sqlalchemy_session',
                            'year', 'start_year_id', 'current_year_id',
                            'password', 'semester_id',
                            'event_id'}
        for field in fields_to_remove:
            if field not in exclude:
                form.pop(field, None)  # Remove the field if it exists

    @staticmethod
    def additional_fields(form: dict, add: dict | None):
        """Adds fields to a form."""
        if add is None:
            add = {}

        for key, value in add.items():
            form[key] = value

    def factory(self, add: dict | None = None, keep: set | None = None, **kwargs):
        self._set_session()

        form = self.Factory.create(**kwargs).to_dict()

        MakeFactory.additional_fields(form, add)
        MakeFactory.modify_fields(form, exclude=keep)

        return form
