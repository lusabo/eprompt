import json
from db import Base, SessionLocal
from sqlalchemy import Column, Integer, String, Text

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    assignee = Column(String(255), nullable=False)
    
    @classmethod
    def _get_database_session(cls):
        return SessionLocal()

    @classmethod
    def save_task_from_json(cls, json_text):
        try:
            task_data = json.loads(json_text)
        except json.JSONDecodeError as e:
            print(f"Erro ao decodificar JSON: {e}")
            return

        session = cls._get_database_session()

        try:
            task = cls(
                title=task_data['titulo'],
                description=task_data.get('descricao', ''),
                assignee=task_data['responsavel']
            )

            session.add(task)
            session.commit()
            print("Task salva com sucesso!")
        except Exception as e:
            session.rollback()
            print(f"Erro ao salvar a Task: {e}")
        finally:
            session.close()
