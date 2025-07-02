from datetime import datetime
from pyethiodate import EthDate  # type: ignore
from sqlalchemy import select
from sqlalchemy.orm import scoped_session, Session
from models.year import Year


class DefaultFelids:
    def __init__(self, session: scoped_session[Session]):
        self.session: scoped_session[Session] = session

    def set_year_id(self) -> str | None:
        year_id = self.session.execute(select(Year.id)).scalar_one_or_none()
        return year_id

    @staticmethod
    def current_EC_year() -> EthDate:
        return EthDate.date_to_ethiopian(datetime.now()).year
