from typing import List
import fastapi as _fastapi
import sqlalchemy.orm as _orm
import src.services as _services
import src.schemas as _schemas
import src.database as _database


router = _fastapi.APIRouter(prefix="/contacts", tags=["contacts"])


@router.get("/", response_model=List[_schemas.Contact])
async def get_contacts(db: _orm.Session = _fastapi.Depends(_database.base.get_db)):
    try:
        return await _services.ContactService.get_all_contacts(db=db)
    except Exception as e:
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/{contact_id}/", response_model=_schemas.Contact)
async def get_contact(contact_id: int, db: _orm.Session = _fastapi.Depends(_database.base.get_db)):
    try:
        contact = await _services.ContactService.get_contact(db=db, contact_id=contact_id)
        if contact is None:
            raise _fastapi.HTTPException(status_code=404, detail="Contact does not exist")
        return contact
    except Exception as e:
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/", response_model=_schemas.Contact)
async def create_contact(contact: _schemas.CreateContact, db: _orm.Session = _fastapi.Depends(_database.base.get_db)):
    try:
        return await _services.ContactService.create_contact(db=db, contact=contact)
    except Exception as e:
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.put("/{contact_id}/", response_model=_schemas.Contact)
async def update_contact(contact_id: int, contact_data: _schemas.CreateContact, db: _orm.Session = _fastapi.Depends(_database.base.get_db)):
    try:
        contact = await _services.ContactService.get_contact(db=db, contact_id=contact_id)
        if contact is None:
            raise _fastapi.HTTPException(status_code=404, detail="Contact does not exist")
        return await _services.ContactService.update_contact(db=db, contact_data=contact_data, contact=contact)
    except Exception as e:
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/{contact_id}/")
async def delete_contact(contact_id: int, db: _orm.Session = _fastapi.Depends(_database.base.get_db)):
    try:
        contact = await _services.ContactService.get_contact(db=db, contact_id=contact_id)
        if contact is None:
            raise _fastapi.HTTPException(status_code=404, detail="Contact does not exist")
        await _services.ContactService.delete_contact(db=db, contact=contact)
        return "successfully deleted the user"
    except Exception as e:
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
