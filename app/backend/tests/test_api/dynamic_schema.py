from typing import Iterable, Literal, Optional, Type, List, Dict, Any, cast
from pydantic import BaseModel, TypeAdapter, ValidationError
from pydantic import ConfigDict

from extension.functions.helper import to_camel
from extension.pydantic.response.schema import SuccessResponseSchema


class DynamicSchema:
    @staticmethod
    def create_dynamic_model(
        base_model: Type[BaseModel],
        include_fields: List[str],
        *,
        extra_config: Optional[ConfigDict] = None,
    ) -> Type[BaseModel]:
        """
        Creates a dynamic Pydantic model containing only specified fields.

        Args:
            base_model: The original model to derive fields from
            include_fields: List of field names to include
            extra_config: Additional model configuration

        Returns:
            A new Pydantic model class
        """
        # Set default config
        config: ConfigDict = {
            "extra": "forbid",
            "alias_generator": to_camel,
            "populate_by_name": True,
        }

        # Merge with any extra config
        if extra_config:
            config.update(extra_config)

        # Create dynamic class
        DynamicModel = type(
            f"Dynamic{base_model.__name__}",
            (BaseModel,),
            {
                "model_config": config,
                "__annotations__": {
                    field: base_model.model_fields[field].annotation
                    for field in include_fields
                    if field in base_model.model_fields
                },
            },
        )
        return cast(Type[BaseModel], DynamicModel)

    @classmethod
    def validate_response(
        cls,
        response_data: Dict[str, Any],
        base_model: Type[BaseModel],
        expected_fields: List[str],
        type: Literal["list", "dict"] = "dict",
    ) -> None:
        """
        Validates API response against a dynamic schema.

        Args:
            response_data: JSON response data to validate
            base_model: Original model class
            expected_fields: Fields that should be present

        Raises:
            AssertionError: If validation fails
        """

        # ensure id is always included
        expected_fields = list(set(expected_fields) | {"id"})

        DynamicModel = cls.create_dynamic_model(base_model, expected_fields)

        try:
            if type == "list":
                # If the response is a list, we expect a list of dynamic models
                Validator = SuccessResponseSchema[List[DynamicModel], None, None]  # type: ignore
                validated_response = Validator.model_validate(response_data)
                assert isinstance(validated_response.data, list), (
                    "Expected data to be a list"
                )
                list_data = cast(List[BaseModel], validated_response.data)

                assert list_data is not None, "Validated data is None"

                # Verify all expected fields are present and no extras
                for item in list_data:
                    assert set(item.model_dump(by_alias=False).keys()) == set(
                        expected_fields
                    )
            else:
                # If the response is a dict, we expect a single dynamic model
                Validator = SuccessResponseSchema[DynamicModel, None, None]  # type: ignore
                validated_response = Validator.model_validate(response_data)

                dict_data = cast(BaseModel, validated_response.data)

                assert dict_data is not None, "Validated data is None"

                # Verify all expected fields are present and no extras
                assert set(dict_data.model_dump(by_alias=False).keys()) == set(
                    expected_fields
                )

        except ValidationError as e:
            errors = "\n".join(f"{err['loc']}: {err['msg']}" for err in e.errors())
            raise AssertionError(
                f"Validation failed for {base_model.__name__}.\n"
                f"Expected fields{expected_fields}.\n"
                f"Response data: {response_data}\n"
                f"Errors:\n{errors}"
            )
