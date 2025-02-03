from sqlalchemy.orm import Session

from fastapi import APIRouter, Depends, HTTPException, Response, status

from .. import database, models, oauth2, schemas

router = APIRouter(prefix="/vote", tags=["Vote"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(
    vote: schemas.Vote,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    post = db.query(models.Post).filter(models.Post.id == vote.id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {vote.id} was not found",
        )

    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == vote.id,
        models.Vote.user_id == current_user.id,
    )
    found_vote = vote_query.first()

    if vote.dir == 1:
        if found_vote:
            return
        new_vote = models.Vote(post_id=vote.id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        db.refresh(new_vote)
        return {"message": "successfully added vote"}
    else:
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "successfully removed vote"}
