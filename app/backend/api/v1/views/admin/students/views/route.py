import json
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

        load_schema = ValidQuerySchema(exclude=("view_id",))
        valid_query = load_schema.load(data)

        # Save the valid query to the database
        new_view = SavedQueryView(
            user_id=admin_data.id,
            name=valid_query["name"],
            table_name=valid_query["table_name"],
            query_json=valid_query["search_params"],
        )
        new_view.save()

        return jsonify(
            {"message": "View Saved Successfully!", "viewId": new_view.id}
        ), 201

    except ValidationError as e:
        return errors.handle_validation_error(e)
    except Exception as e:
        return errors.handle_internal_error(e)


@admin.route("/rename-view", methods=["PUT"])
@admin_required
def rename_view(admin_data: UserT) -> Tuple[Response, int]:
    """
    Rename an existing student view.
    """

    try:
        data = request.get_json()

        load_schema = ValidQuerySchema(only=("view_id", "name"))
        valid_query = load_schema.load(data)

        view_id = valid_query["view_id"]
        new_name = valid_query["name"]

        # Fetch the saved view by ID
        view = storage.session.query(SavedQueryView).filter_by(id=view_id).first()
        if not view:
            return jsonify({"message": "View not found"}), 404

        # Update the view name
        view.name = new_name
        view.save()

        return jsonify({"message": "View Renamed Successfully!"}), 200

    except ValidationError as e:
        return errors.handle_validation_error(e)
    except Exception as e:
        return errors.handle_internal_error(e)


@admin.route("/update-view", methods=["PUT"])
@admin_required
def update_view(admin_data: UserT) -> Tuple[Response, int]:
    """
    Update an existing student view by its ID.
    """

    try:
        data = request.get_json()

        load_schema = ValidQuerySchema()
        valid_query = load_schema.load(data)

        view = (
            storage.session.query(SavedQueryView)
            .filter_by(id=valid_query["view_id"])
            .first()
        )

        if not view:
            return jsonify({"message": "View not found"}), 404
        print(valid_query)
        view.query_json = {
            **valid_query["search_params"],
            "columns": valid_query.get("columns", []),
        }

        view.save()

        return jsonify(
            {"message": "View Updated Successfully!", "viewId": view.id}
        ), 200
    except ValidationError as e:
        return errors.handle_validation_error(e)
    except Exception as e:
        return errors.handle_internal_error(e)


@admin.route("/delete-view/<view_id>", methods=["PUT"])
@admin_required
def delete_view(admin_data: UserT, view_id: str) -> Tuple[Response, int]:
    """
    Delete an existing student view by its ID.
    """

    try:
        if not view_id or not isinstance(view_id, str):
            return jsonify({"message": "Invalid view ID Type"}), 400

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
                "table_name": view.table_name.value,
                "columns": list(view.query_json.pop("columns", [])),
                "search_params": view.query_json,
                "created_at": view.created_at,
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
