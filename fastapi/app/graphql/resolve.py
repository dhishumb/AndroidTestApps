from graphene import ObjectType, List, String, Schema
from .schema import CourseType
import json
import os


class Query(ObjectType):
    course_list = None
    get_course = List(CourseType)

    async def resolve_get_course(self, info):
        filepath = os.path.join(os.getcwd(), "app", "graphql", "courses.json")
        with open(filepath) as courses:
            course_list = json.load(courses)
        return course_list
