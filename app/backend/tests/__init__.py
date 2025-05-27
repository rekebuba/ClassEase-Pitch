from api import create_app
from models import storage


test_app = create_app("testing")
storage.init_app(test_app)
