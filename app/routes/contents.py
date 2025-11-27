from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai_service import AIService
from app.auth import get_current_user
from app.deps import get_ai_service, get_db
from app.models import Content, User
from app.schemas import ContentCreate, ContentOut, ContentUpdate

router = APIRouter(prefix="/contents", tags=["contents"])


async def _get_content_or_404(session: AsyncSession, content_id: int, owner_id: int) -> Content:
    result = await session.execute(
        select(Content).where(Content.id == content_id, Content.owner_id == owner_id)
    )
    content = result.scalar_one_or_none()
    if not content:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Content not found")
    return content


@router.post("/", response_model=ContentOut, status_code=status.HTTP_201_CREATED)
async def create_content(
    payload: ContentCreate,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    ai_service: AIService = Depends(get_ai_service),
) -> Content:
    content = Content(title=payload.title, body=payload.body, owner_id=current_user.id)
    session.add(content)
    await session.commit()
    await session.refresh(content)

    ai_result = await ai_service.summarize_and_analyze(payload.body)
    content.summary = ai_result.summary
    content.sentiment = ai_result.sentiment
    content.sentiment_score = ai_result.sentiment_score
    await session.commit()
    await session.refresh(content)
    return content


@router.get("/", response_model=list[ContentOut])
async def list_contents(
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[Content]:
    result = await session.execute(select(Content).where(Content.owner_id == current_user.id))
    return result.scalars().all()


@router.get("/{content_id}", response_model=ContentOut)
async def get_content(
    content_id: int,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Content:
    return await _get_content_or_404(session, content_id, current_user.id)


@router.put("/{content_id}", response_model=ContentOut)
async def update_content(
    content_id: int,
    payload: ContentUpdate,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    ai_service: AIService = Depends(get_ai_service),
) -> Content:
    content = await _get_content_or_404(session, content_id, current_user.id)
    body_updated = False

    if payload.title is not None:
        content.title = payload.title
    if payload.body is not None:
        content.body = payload.body
        body_updated = True

    if body_updated:
        ai_result = await ai_service.summarize_and_analyze(content.body)
        content.summary = ai_result.summary
        content.sentiment = ai_result.sentiment
        content.sentiment_score = ai_result.sentiment_score

    await session.commit()
    await session.refresh(content)
    return content


@router.delete("/{content_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_content(
    content_id: int,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    content = await _get_content_or_404(session, content_id, current_user.id)
    await session.delete(content)
    await session.commit()

