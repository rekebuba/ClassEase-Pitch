from marshmallow import fields, ValidationError
from models import storage
from models.year import Year


class YearIdField(fields.Field):
    """Custom field to fetch year_id based on academic_year."""

    def _deserialize(self, value, attr, data, **kwargs):
        academic_year = data.get('academic_year')
        if academic_year is None:
            raise ValidationError("academic_year is required")

        # Fetch the year_id from the database
        year_id = storage.session.query(Year.id).filter_by(
            ethiopian_year=academic_year
        ).scalar()

        if year_id is None:
            raise ValidationError(
                f"No Year found for academic_year: {academic_year}")

        return year_id
