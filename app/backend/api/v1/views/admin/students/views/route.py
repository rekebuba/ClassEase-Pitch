from typing import Tuple

from flask import Response, jsonify, request
from marshmallow import ValidationError
from api.v1.utils.typing import UserT
from api.v1.views import errors
from api.v1.views.admin.students.views.schema import AllStudentViews, ValidQuerySchema
from api.v1.views.utils import admin_required
from api.v1.views.admin import admins as admin
from models.saved_query_view import SavedQueryView
from models import storage


@admin.route("/views", methods=["POST"])
@admin_required
def create_new_views(admin_data: UserT) -> Tuple[Response, int]:
    """
    Save a new student view based on the provided query parameters.
    """
    try:
        data = request.get_json()

        load_schema = ValidQuerySchema()
        valid_query = load_schema.load(data)

        # Save the valid query to the database
        SavedQueryView(
            user_id=admin_data.id,
            name=valid_query.pop("name"),
            table_name=valid_query.pop("table_name"),
            query_json=valid_query,
        ).save()

        return jsonify({"message": "View Saved Successfully!"}), 201

    except ValidationError as e:
        return errors.handle_validation_error(e)
    except Exception as e:
        return errors.handle_internal_error(e)


@admin.route("/update-view/<table_name>/<view_id>", methods=["PUT"])
@admin_required
def update_view(
    admin_data: UserT, table_name: str, view_id: str
) -> Tuple[Response, int]:
    """
    Update an existing student view by its ID.
    """

    try:
        # Validate the view ID
        if not view_id and not isinstance(view_id, str):
            return jsonify({"message": "Invalid view ID"}), 400

        view = storage.session.query(SavedQueryView).filter_by(id=view_id).first()
        if not view:
            return jsonify({"message": "View not found"}), 404

        data = request.get_json()

        load_schema = ValidQuerySchema()
        valid_query = load_schema.load({**data, "table_name": table_name})

        valid_query.pop("table_name")
        new_name = valid_query.pop("name")
        rename = data.get("name")

        if rename:
            # Update the existing view with the new name
            view.name = new_name
        else:
            view.query_json = valid_query

        view.save()

        return jsonify(
            {"message": f"View {'Renamed' if rename else 'Updated'} Successfully!"}
        ), 200
    except ValidationError as e:
        return errors.handle_validation_error(e)
    except Exception as e:
        return errors.handle_internal_error(e)


@admin.route("/delete-view/<table_name>/<view_id>", methods=["PUT"])
@admin_required
def delete_view(
    admin_data: UserT, table_name: str, view_id: str
) -> Tuple[Response, int]:
    """
    Delete an existing student view by its ID.
    """

    try:
        # Validate the view ID
        if not view_id and not isinstance(view_id, str):
            return jsonify({"message": "Invalid view ID"}), 400

        view = storage.session.query(SavedQueryView).filter_by(id=view_id).first()
        if not view:
            return jsonify({"message": "View not found"}), 404

        # Delete the saved view
        storage.session.delete(view)
        storage.session.commit()

        return jsonify({"message": "View Deleted Successfully!"}), 200

    except ValidationError as e:
        return errors.handle_validation_error(e)
    except Exception as e:
        return errors.handle_internal_error(e)


@admin.route("/all-views/<table_name>", methods=["GET"])
@admin_required
def all_views(admin_data: UserT, table_name: str) -> Tuple[Response, int]:
    """
    Retrieve and return the views of students.
    """

    try:
        # Validate the table name
        load_schema = ValidQuerySchema(only=("table_name",))
        table_name_enum = load_schema.load({"table_name": table_name})

        # Fetch all saved views for the admin user
        saved_views = (
            storage.session.query(SavedQueryView).filter_by(
                user_id=admin_data.id, table_name=table_name_enum["table_name"]
            )
        ).all()

        if not saved_views:
            return jsonify([]), 200

        # Prepare the response data
        response_data = [
            {
                "view_id": view.id,
                "name": view.name,
                "columns": list(view.query_json.get("columns", [])),
                "created_at": view.created_at,
                "updated_at": view.updated_at,
            }
            for view in saved_views
        ]

        dump_schema = AllStudentViews(many=True)
        valid_dump = dump_schema.dump(response_data)

        return jsonify(valid_dump), 200

    except ValidationError as e:
        return errors.handle_validation_error(e)
    except Exception as e:
        return errors.handle_internal_error(e)


@admin.route("/view/<view_id>", methods=["GET"])
@admin_required
def single_view(admin_data: UserT, view_id: str) -> Tuple[Response, int]:
    """
    Retrieve a single student view by its ID.
    """

    try:
        # Validate the view ID
        if not view_id and not isinstance(view_id, str):
            return jsonify({"message": "Invalid view ID"}), 400

        # Fetch the saved view for the admin user
        saved_view = (
            storage.session.query(SavedQueryView)
            .filter_by(user_id=admin_data.id, id=view_id)
            .first()
        )

        if not saved_view:
            return jsonify({"message": "View not found"}), 404

        # Prepare the response data
        response_data = {
            "view_id": saved_view.id,
            "name": saved_view.name,
            "columns": list(saved_view.query_json.pop("columns", [])),
            "query_parameters": saved_view.query_json,
            "created_at": saved_view.created_at,
            "updated_at": saved_view.updated_at,
        }

        dump_schema = AllStudentViews()
        valid_dump = dump_schema.dump(response_data)

        return jsonify(valid_dump), 200

    except ValidationError as e:
        return errors.handle_validation_error(e)
    except Exception as e:
        return errors.handle_internal_error(e)
