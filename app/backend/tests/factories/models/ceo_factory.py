from faker import Faker
from models.ceo import CEO
from .base_factory import BaseFactory

fake = Faker()


class CEOFactory(BaseFactory[CEO]):
    class Meta:
        model = CEO

    identification
