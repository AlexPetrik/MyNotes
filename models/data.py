import os

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from models.note import Base, Note

db_path = "sqlite:///mynotes.db"

def create_test_data():
    if not os.path.exists("mynotes.db"):
        engine = create_engine(db_path, echo=True)
        Base.metadata.create_all(engine)

        with Session(engine) as session:
            data = []
            for i in range(0, 10):
                note = Note(
                    header = f"Header {i}",
                    description = f"Description {i}" * 10
                )
                data.append(note)

            session.add_all(data)
            session.commit()

def get_data():
    create_test_data()
    
    engine = create_engine(db_path, echo=True)
    with Session(engine) as session:
        all_notes = session.query(Note).all()
        notes_arr = []
        for note in all_notes:
            note_arr = [note.id, note.header, note.description]
            notes_arr.append(note_arr)

        return notes_arr