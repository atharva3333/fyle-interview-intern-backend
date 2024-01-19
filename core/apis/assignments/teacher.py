from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment

from .schema import AssignmentSchema, AssignmentGradeSchema
teacher_assignments_resources = Blueprint('teacher_assignments_resources', __name__)


# @teacher_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
# @decorators.authenticate_principal
# def list_assignments(p):
#     """Returns list of assignments"""
#     teachers_assignments = Assignment.get_assignments_by_teacher(p.teacher_id)
#     teachers_assignments_dump = AssignmentSchema().dump(teachers_assignments, many=True)
#     return APIResponse.respond(data=teachers_assignments_dump)

@teacher_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(p):
    """Returns list of assignments excluding DRAFT"""
    # Get assignments excluding those in the DRAFT state
    teachers_assignments = Assignment.filter(Assignment.teacher_id == p.teacher_id, Assignment.state != 'DRAFT').all()

    # Serialize the assignments
    teachers_assignments_dump = AssignmentSchema().dump(teachers_assignments, many=True)

    # Return the API response
    return APIResponse.respond(data=teachers_assignments_dump)



@teacher_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_assignment(p, incoming_payload):
    """Grade an assignment"""
    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)


    assignment = Assignment.get_by_id(grade_assignment_payload.id)
    if not assignment:
        return APIResponse.respond_error('FyleError', status_code=404)

    # Check if the assignment belongs to the teacher
    assignment_belongs_to_teacher = Assignment.filter(
        Assignment.id == grade_assignment_payload.id,
        Assignment.teacher_id == p.teacher_id
    ).first()

    if not assignment_belongs_to_teacher:
        return APIResponse.respond_error('FyleError', status_code=400)

    graded_assignment = Assignment.mark_grade(
        _id=grade_assignment_payload.id,
        grade=grade_assignment_payload.grade,
        auth_principal=p
    )
    db.session.commit()
    graded_assignment_dump = AssignmentSchema().dump(graded_assignment)
    return APIResponse.respond(data=graded_assignment_dump)

