import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from app.api.deps import CurrentUser, SessionDep
from app.models import (
    Assignment,
    AssignmentCreate,
    AssignmentPublic,
    AssignmentsPublic,
    AssignmentUpdate,
    Message,
)
from app.utils.cache import delete_cache, get_cache, set_cache

router = APIRouter(prefix="/assignments", tags=["assignments"])


@router.get("/", response_model=AssignmentsPublic)
def read_assignments(
    session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve assignments (cached for speed).
    """
    
    cache_key = f"user:{current_user.id}:assignments:skip:{skip}:limit:{limit}"
    
   
    cached = get_cache(cache_key)
    if cached:
        return cached  
    
    
    count_statement = (
        select(func.count())
        .select_from(Assignment)
        .where(Assignment.owner_id == current_user.id)
    )
    count = session.exec(count_statement).one()
    
    statement = (
        select(Assignment)
        .where(Assignment.owner_id == current_user.id)
        .order_by(Assignment.due_date.asc())
        .offset(skip)
        .limit(limit)
    )
    assignments = session.exec(statement).all()
    
    result = AssignmentsPublic(data=assignments, count=count)
    
   
    set_cache(cache_key, result.model_dump())
    
    return result


@router.post("/", response_model=AssignmentPublic)
def create_assignment(
    *, session: SessionDep, current_user: CurrentUser, assignment_in: AssignmentCreate
) -> Any:
    """
    Create new assignment and clear cache.
    """
    assignment = Assignment.model_validate(
        assignment_in, update={"owner_id": current_user.id}
    )
    session.add(assignment)
    session.commit()
    session.refresh(assignment)
    
    delete_cache(f"user:{current_user.id}:assignments:skip:0:limit:100")
    
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
    Update an assignment and clear cache.
    """
    assignment = session.get(Assignment, id)
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    
    if assignment.owner_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
        
    update_dict = assignment_in.model_dump(exclude_unset=True)
    assignment.sqlmodel_update(update_dict)
    session.add(assignment)
    session.commit()
    session.refresh(assignment)
    
    delete_cache(f"user:{current_user.id}:assignments:skip:0:limit:100")
    
    return assignment


@router.delete("/{id}")
def delete_assignment(
    session: SessionDep, current_user: CurrentUser, id: uuid.UUID
) -> Message:
    """
    Delete an assignment and clear cache.
    """
    assignment = session.get(Assignment, id)
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
        
    if assignment.owner_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
        
    session.delete(assignment)
    session.commit()
    
    # Clear cache
    delete_cache(f"user:{current_user.id}:assignments:skip:0:limit:100")
    
    return Message(message="Assignment deleted successfully")