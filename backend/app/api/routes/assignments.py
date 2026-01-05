import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

# 1. Add CurrentUser dependency
from app.api.deps import CurrentUser, SessionDep
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
    session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve assignments (only for current user).
    """
    # Filter by owner_id
    count_statement = (
        select(func.count())
        .select_from(Assignment)
        .where(Assignment.owner_id == current_user.id)
    )
    count = session.exec(count_statement).one()
    
    # Filter by owner_id and sort
    statement = (
        select(Assignment)
        .where(Assignment.owner_id == current_user.id)
        .order_by(Assignment.due_date.asc())
        .offset(skip)
        .limit(limit)
    )
    assignments = session.exec(statement).all()
    
    return AssignmentsPublic(data=assignments, count=count)

@router.post("/", response_model=AssignmentPublic)
def create_assignment(
    *, session: SessionDep, current_user: CurrentUser, assignment_in: AssignmentCreate
) -> Any:
    """
    Create new assignment (linked to current user).
    """
   
    assignment = Assignment.model_validate(
        assignment_in, update={"owner_id": current_user.id}
    )
    session.add(assignment)
    session.commit()
    session.refresh(assignment)
    return assignment

@router.patch("/{id}", response_model=AssignmentPublic)
def update_assignment(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    id: uuid.UUID,
    assignment_in: AssignmentUpdate,
) -> Any:
    """
    Update an assignment (if owned by user).
    """
    assignment = session.get(Assignment, id)
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    
    # Security Check
    if assignment.owner_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
        
    update_dict = assignment_in.model_dump(exclude_unset=True)
    assignment.sqlmodel_update(update_dict)
    session.add(assignment)
    session.commit()
    session.refresh(assignment)
    return assignment

@router.delete("/{id}")
def delete_assignment(
    session: SessionDep, current_user: CurrentUser, id: uuid.UUID
) -> Message:
    """
    Delete an assignment (if owned by user).
    """
    assignment = session.get(Assignment, id)
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
        
    # Security Check
    if assignment.owner_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
        
    session.delete(assignment)
    session.commit()
    return Message(message="Assignment deleted successfully")