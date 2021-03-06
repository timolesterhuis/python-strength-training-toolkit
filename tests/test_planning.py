from streprogen import Program, Day, DynamicExercise, StaticExercise
from strengthtrainingtoolkit.database import Base, ExerciseDescription
from strengthtrainingtoolkit.planning import program_to_sql
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
import os


@contextmanager
def temporary_db(path, delete=True):
    yield
    if delete:
        try:
            os.remove(path)
        except:
            pass


def create_memory_session():
    engine = create_engine("sqlite:///:memory:", echo=True)

    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


def test_single_program():
    session = create_memory_session()

    # Create a 4-week program
    program = Program('My first program!', duration=4)

    # Create some dynamic and static exercises
    bench = DynamicExercise('Bench press',
                            start_weight=60, final_weight=80)
    squats = DynamicExercise('Squats',
                             start_weight=80, final_weight=95)
    curls = StaticExercise('Curls', '3 x 12')
    day = Day(exercises=[bench, squats, curls])

    # Add day(s) to program and render it
    program.add_days(day)
    program.render()

    p = program_to_sql(program)
    return session, program, p


def test_exercisedescription_program():

    with temporary_db("tempfile.db", delete=False):
        engine = create_engine("sqlite:///tempfile.db", echo=True)

        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()

        ed = ExerciseDescription(name="Bench press", description="Let's see if this works!")
        session.add(ed)
        session.commit()
        #del session

        # Create a 4-week program
        program = Program('My first program!', duration=4)

        # Create some dynamic and static exercises
        bench = DynamicExercise('Bench press',
                                start_weight=60, final_weight=80)
        squats = DynamicExercise('Squats',
                                 start_weight=80, final_weight=95)
        curls = StaticExercise('Curls', '3 x 12')
        day = Day(exercises=[bench, squats, curls])

        # Add day(s) to program and render it
        program.add_days(day)
        program.render()

        p = program_to_sql(program, engine=engine)
        #session = Session()
        session.commit()
    return program, p


if __name__ == "__main__":
    test_single_program()
    test_exercisedescription_program()
