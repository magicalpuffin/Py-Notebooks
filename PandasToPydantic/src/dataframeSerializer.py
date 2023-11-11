import pandas as pd
from pydantic import BaseModel
import types
from typing import Union


def expandAnnotation(model: BaseModel):
    if not model.__base__ == BaseModel:
        raise TypeError(f"{model} is not a BaseModel")

    annotations = model.__annotations__.copy()

    for key, fieldType in annotations.items():
        if type(fieldType) == types.GenericAlias:
            # Only expanding lists
            if fieldType.__origin__ == list:
                # Using lists to indicate list structure
                annotations[key] = [expandAnnotation(fieldType.__args__[0])]

    return annotations


def getBaseFields(structure: dict) -> list[str]:
    baseFields = []

    for k, v in structure.items():
        if type(v) != list:
            baseFields.append(k)

    return baseFields


def getListFields(structure: dict) -> list[str]:
    listFields = []

    for k, v in structure.items():
        if type(v) == list:
            listFields.append(k)

    return listFields


def serializeDataframe(data: pd.DataFrame, structure: dict):
    newList = []
    baseFields = getBaseFields(structure)
    listFields = getListFields(structure)
    # Assumes first field is id
    idField = baseFields[0]

    if not listFields:
        # Might be bad design, should ensure unique id
        return data[baseFields].to_dict(orient="records")

    for value in data[idField].unique():
        sliceData = data[data[idField] == value]

        baseDict = sliceData[baseFields].iloc[0].to_dict()

        if listFields:
            baseDict[listFields[0]] = serializeDataframe(
                sliceData, structure[listFields[0]][0]
            )

        newList.append(baseDict)

    return newList
