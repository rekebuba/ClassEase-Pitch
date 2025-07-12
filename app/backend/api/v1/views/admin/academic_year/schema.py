from pydantic import BaseModel, ConfigDict

from extension.functions.helper import to_camel


class SectionForGrade(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )
    
    
