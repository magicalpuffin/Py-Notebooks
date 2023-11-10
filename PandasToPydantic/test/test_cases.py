import pytest
from pydantic import BaseModel
from PandasToPydantic.src.dataframeSerializer import (
    expandAnnotation,
    getBaseFields,
    getListFields,
    serializeDataframe,
)


class GrandChildModel(BaseModel):
    grandChildString: str
    grandChildInteger: int


class ChildModel(BaseModel):
    childString: str
    childInteger: int
    childListGrandChild: list[GrandChildModel]


class ParentModel(BaseModel):
    parentString: str
    parentInteger: int
    parentFloat: float
    parentListChild: list[ChildModel]


class BaseModelErrorModel(BaseModel):
    modelErrorList: list[str]


class Test_expandAnnotation:
    def test_GrandChildModel(self):
        expanded = expandAnnotation(GrandChildModel)
        target = {
            "grandChildString": str,
            "grandChildInteger": int,
        }
        assert expanded == target

    def test_ChildModel(self):
        expanded = expandAnnotation(ChildModel)
        target = {
            "childString": str,
            "childInteger": int,
            "childListGrandChild": [expandAnnotation(GrandChildModel)],
        }
        assert expanded == target

    def test_ParentModel(self):
        expanded = expandAnnotation(ParentModel)
        target = {
            "parentString": str,
            "parentInteger": int,
            "parentFloat": float,
            "parentListChild": [expandAnnotation(ChildModel)],
        }
        assert expanded == target

    def test_BaseModelError(self):
        with pytest.raises(TypeError):
            expandAnnotation(BaseModelErrorModel)
