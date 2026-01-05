import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from app.api.deps import SessionDep
from app.models import (
    Assignment,
    AssignmentCreate,
    AssignmentPublic,
    AssignmentsPublic,
    AssignmentUpdate,
    Message,
)

router = APIRouter(prefix="/assignments", tags=["assignments"])


@router.get("/", response_model=AssignmentsPublic)
def read_assignments(
    session: SessionDep, skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve assignments from database.
    """
    count_statement = select(func.count()).select_from(Assignment)
    count = session.exec(count_statement).one()
    
    # Sort by due_date ascending (Soonest due date first)
    statement = select(Assignment).order_by(Assignment.due_date.asc()).offset(skip).limit(limit)
    assignments = session.exec(statement).all()
    
    return AssignmentsPublic(data=assignments, count=count)


@router.post("/", response_model=AssignmentPublic)
def create_assignment(
    *, session: SessionDep, assignment_in: AssignmentCreate
) -> Any:
    """
    Create new assignment in database.
    """
    assignment = Assignment.model_validate(assignment_in)
    session.add(assignment)
    session.commit()
    session.refresh(assignment)
    return assignment


@router.patch("/{id}", response_model=AssignmentPublic)
def update_assignment(
    *, session: SessionDep, id: uuid.UUID, assignment_in: AssignmentUpdate
) -> Any:
    """
    Update an assignment in database.
    """
    assignment = session.get(Assignment, id)
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
        
    update_dict = assignment_in.model_dump(exclude_unset=True)
    assignment.sqlmodel_update(update_dict)
    session.add(assignment)
    session.commit()
    session.refresh(assignment)
    return assignment


@router.delete("/{id}")
def delete_assignment(session: SessionDep, id: uuid.UUID) -> Message:
    """
    Delete an assignment from database.
    """
    assignment = session.get(Assignment, id)
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
        
    session.delete(assignment)
    session.commit()
    return Message(message="Assignment deleted successfully")
