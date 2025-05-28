from typing import Tuple

from flask import Response, jsonify, request
from marshmallow import ValidationError
from sqlalchemy import and_
from api.v1.utils.typing import UserT
from api.v1.views.admin import admins as admin
from api.v1.views.utils import admin_required
from api.v1.views.admin.event.schema import AvailableEventsSchema, EventSchema
from models.semester import Semester
from models.year import Year
from models.event import Event
from models import storage
from api.v1.views import errors


@admin.route("/events", methods=["GET"])
@admin_required
def available_events(admin_data: UserT) -> Tuple[Response, int]:
    """
    Handle retrieval of events.
    """
    try:
        events = storage.session.query(Event).all()

        if not events:
            return errors.handle_not_found_error("No event found")

        schema = AvailableEventsSchema()
        result = schema.dump({"events": events})

        return jsonify(result), 200
    except ValidationError as e:
        return errors.handle_validation_error(e)
    except Exception as e:
        return errors.handle_internal_error(e)


@admin.route("/event/new", methods=["POST"])
@admin_required
def create_events(admin_data: UserT) -> Tuple[Response, int]:
    try:
        data = request.get_json()
        event_schema = EventSchema()
        validated_data = event_schema.load(data)

        # extract any nested felids
        semester = validated_data.pop("semester", None)

        new_event = Event(**validated_data)
        storage.add(new_event)
        storage.session.flush()

        if new_event.purpose == "New Semester":
            semester_data = {
                **semester,
                "event_id": new_event.id,
            }

            # check for duplicate event
            existing_event = (
                storage.session.query(Event, Semester, Year)
                .join(Semester, Semester.event_id == Event.id)
                .join(Year, Year.id == Event.year_id)
                .filter(
                    and_(
                        Event.purpose == new_event.purpose,
                        Event.organizer == new_event.organizer,
                    )
                )
            )

            new_semester = Semester(**semester_data)
            storage.add(new_semester)

        storage.save()

        return event_schema.dump({"message": "Event Created Successfully"}), 201
    except ValidationError as e:
        storage.rollback()
        return errors.handle_validation_error(e)
    except Exception as e:
        storage.rollback()
        return errors.handle_internal_error(e)
