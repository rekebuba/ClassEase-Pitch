from typing import Dict

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from project.api.v1.routers.year.schema import NewYearSuccess
from project.core.config import settings
from project.models.year import Year
from tests.factories.api_data import NewYearFactory


class TestYearApi:
    def test_create_new_academic_year(
        self,
        client: TestClient,
        admin_token_headers: Dict[str, str],
        db_session: Session,
    ) -> None:
        data = NewYearFactory.create(setup_methods="Default Template")

        r = client.post(
            f"{settings.API_V1_STR}/years",
            json=data.model_dump(mode="json", by_alias=True),
            headers=admin_token_headers,
        )

        assert r.status_code == 201

        result = NewYearSuccess.model_validate_json(r.text)

        assert "Year created Successfully" == result.message

        year = db_session.get(Year, result.id)
        assert year is not None
