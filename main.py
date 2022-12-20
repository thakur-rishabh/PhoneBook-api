# reference: https://www.gormanalysis.com/blog/building-a-simple-crud-application-with-fastapi/

from fastapi import FastAPI, status, HTTPException, Depends, Query
from database import Base, engine, SessionLocal
import sqlalchemy
from sqlalchemy.orm import Session
import re
import logging
import models
import schemas
import socket

# logginf configuration
hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)
log_level = logging.INFO
logging.basicConfig(filename="audit.log",
                    level=log_level,
                    format=f"{ip} %(asctime)s %(message)s",
                    filemode="a")

# databse creation
Base.metadata.create_all(engine)

# initialize app
app = FastAPI()

# db session
def get_session():
    try:
        session = SessionLocal()
        yield session
    finally:
        session.close()

# Invalid phone number regex pattern
invalid_phoneNumber = re.compile(r".*[a-zA-Z].+|.*[/].*|[0-9]{10}|^[0-9]{3}$|^[\+][0-9]{4,}.*|^\(001\).*|^[\+][0][1].*|.+[a-z].+")
invalid_name = re.compile(r".*[\*;].*|.*[<><\/>].*|.*[\d].*|.*[’]{2}.*|.*[’].*[-].*[-].*|.*[a-zA-Z][ ].*[a-zA-Z].*[a-zA-Z][ ].*")

# default location
@app.get("/")
def root():
    logging.info("root")
    return {"options": {
            "add": "add user with name and password",
            "deleteByName": "delete the user by name",
            "deleteByPhone": "delete the user by phone number"}}

# Create phone book entry --> post | path: "/PhoneBook/add"
@app.post("/PhoneBook/add", status_code=status.HTTP_200_OK)
def create_phoneBook(add: schemas.phoneBookRequest, 
                    session: Session = Depends(get_session)):
    phonebookdb = models.PhoneBook()
    if bool(invalid_phoneNumber.search(add.phoneNumber)) == True or bool(invalid_name.search(add.name)) == True:
        logging.error(f"400 POST - '{add.phoneNumber}' or '{add.name}' is invalid")
        raise HTTPException(status_code=400, detail={"ERROR": "Invalid name or phone number"})
    else:
        try:
            phonebookdb.phoneNumber = add.phoneNumber
            phonebookdb.name = add.name
            session.add(phonebookdb)
            session.commit()
            session.refresh(phonebookdb)
            session.close()
            logging.info(f"200 POST - {add.phoneNumber} & {add.name} added to phonebook database")
            return {"detail": "user is created"}
        except sqlalchemy.exc.IntegrityError:
            logging.error(f"400 POST - '{add.phoneNumber}' or '{add.name}' are present in phonebook database")
            raise HTTPException(status_code=400, detail={"ERROR": "name or phone number already present"})

# delete phone-book by name --> put | path: "/PhoneBook/deleteByName"
@app.put("/PhoneBook/deleteByName")
def delete_by_name(deleteByName: schemas.deleteByNameRequest,
                    session: Session = Depends(get_session)):
    if bool(invalid_name.search(deleteByName.name)) == True:
        logging.error(f"400 PUT - '{deleteByName.name}' is invalid")
        raise HTTPException(status_code=400, detail={"ERROR": "Invalid name"})
    else:
        entry_to_remove = session.query(models.PhoneBook).where(
            models.PhoneBook.name == deleteByName.name).first()
        if entry_to_remove:
            session.delete(entry_to_remove)
            session.commit()
            session.close()
            logging.info(f"200 PUT - '{deleteByName.name}' is added to phonebook databse")
            return {"detail": "user is removed successfully"}
        else:
            logging.info(f"404 PUT - '{deleteByName.name}' is not present in phonebook databse")
            raise HTTPException(status_code=404, detail={"ERROR": "name is not present"})

# delete phone-book by phone number --> put | path: "/PhoneBook/deleteByNumber"
@app.put("/PhoneBook/deleteByNumber")
def delete_by_number(deleteByNumber: schemas.deleteByNumberRequest,
                    session: Session = Depends(get_session)):
    if bool(invalid_phoneNumber.search(deleteByNumber.phoneNumber)) == True:
        logging.error(f"400 PUT - '{deleteByNumber.phoneNumber}' is invalid phone number")
        raise HTTPException(status_code=400, detail={"ERROR": "Invalid phone number"})
    else:
        entry_to_remove = session.query(models.PhoneBook).where(
            models.PhoneBook.phoneNumber == deleteByNumber.phoneNumber).first()
        if entry_to_remove:
            session.delete(entry_to_remove)
            session.commit()
            session.close()
            logging.info(f"200 PUT - '{deleteByNumber.phoneNumber}' is invalid phone number")
            return {"detail": "user is removed successfully"}
        else:
            logging.info(f"404 PUT - '{deleteByNumber.phoneNumber}' is not present in phone number")
            raise HTTPException(status_code=404, detail="phone number not present")

# read all the entry in phone book --> get | path: "/PhoneBook/list"
@app.get("/PhoneBook/list")
def list_phoneBook(session: Session = Depends(get_session)):
    phoneBook_list = session.query(models.PhoneBook).all()
    session.close()
    logging.info("200 GET - list all the phonebook entry")
    return phoneBook_list