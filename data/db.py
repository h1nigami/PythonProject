from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from data.models import Teacher
from .models import *
from dotenv import load_dotenv
import os
import logging

load_dotenv(verbose=True)

token = str(os.getenv('token'))

owner = os.getenv('owner')

engine = create_engine('sqlite:///database.db')


class DataBase:
    """Класс для работы с базой данных бота, управляющий учителями и группами."""

    def __init__(self):
        """Инициализирует подключение к базе данных и настраивает логгирование."""
        self.Session = sessionmaker(bind=engine)
        self.session = self.Session()
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    @staticmethod
    def create_table():
        """Создает все таблицы в базе данных, если они отсутствуют."""
        Base.metadata.create_all(engine)

    def add_teacher(self, tg_id: int, name: str, is_admin: bool = False) -> None:
        """
        Добавляет нового учителя в базу данных.

        Args:
            tg_id: Telegram ID учителя
            name: Имя учителя
            is_admin: Флаг администратора (по умолчанию False)

        Raises:
            SQLAlchemyError: При ошибках работы с базой данных
        """
        try:
            teacher = Teacher(tg_id=tg_id, name=name, is_admin=is_admin)
            self.session.add(teacher)
            self.session.commit()
            self.session.close()
            self.logger.info(f"Добавлен учитель {name} (ID: {tg_id})")
        except Exception as e:
            self.logger.info(f'Ошибка при добавлении учителя {e}')
            self.session.rollback()
            raise

    def delete_teacher(self, tg_id: int) -> None:
        """
        Удаляет учителя из базы данных
        Args:
            tg_id: Telegram ID

        Raises:
            SQLAlchemyError: Не найден учитель
        """
        try:
            teacher = self.session.query(Teacher).filter_by(tg_id=tg_id).first()
            self.session.delete(teacher)
            self.session.commit()
            self.session.close()
            self.logger.info(f'Удален учитель {teacher.name}')
        except Exception as e:
            self.session.rollback()
            self.logger.info(f'Ошибка при удалении {e}')
            raise

    def get_teacher(self, tg_id: int) -> Teacher | None:
        """
        Возвращает объект учителя по Telegram ID.

        Args:
            tg_id: Telegram ID учителя

        Returns:
            Объект Teacher или None, если учитель не найден

        Raises:
            SQLAlchemyError: При ошибках работы с базой данных
        """
        try:
            teacher = self.session.query(Teacher).filter_by(tg_id=tg_id).first()
            return teacher
        except Exception as e:
            print(e)
            self.session.rollback()
            return None

    @property
    def get_all_teachers(self) -> list[type[Teacher]] | None:
        """
        Возвращает всех учителей
        :return: list с обьектами Teacher
        """
        try:
            teachers = self.session.query(Teacher).all()
            return teachers
        except Exception as e:
            self.logger.info(f'Ошибка: {e}')
            self.session.rollback()
            return None

    def subtract_score(self, tg_id: int, value: int) -> None:
        """
        Уменьшает баллы учителя на указанное значение.

        Args:
            tg_id: Telegram ID учителя
            value: Количество баллов для вычитания

        Raises:
            SQLAlchemyError: При ошибках работы с базой данных
        """
        try:
            teacher = self.session.query(Teacher).filter_by(tg_id=tg_id).first()
            teacher.score -= value
            self.session.commit()
            self.session.close()
        except:
            self.session.rollback()
        finally:
            self.session.close()

    def add_admin(self, tg_id: int, name: str, group: Group | None = None) -> None:
        """
        Добавляет администратора с возможностью привязки к группе.

        Args:
            tg_id: Telegram ID администратора
            name: Имя администратора
            group: Объект Group (опционально)

        Raises:
            SQLAlchemyError: При ошибках работы с базой данных
        """
        try:
            if group is None:
                admin = Teacher(tg_id, name, is_admin=True)
                self.session.add(admin)
                self.session.commit()
                self.session.close()
            else:
                admin = Teacher(tg_id, name, group, is_admin=True)
                self.session.add(admin)
                self.session.commit()
                self.session.close()
        except:
            self.session.rollback()
        finally:
            self.session.close()

    def is_admin(self, tg_id: int) -> bool:
        """
        Проверяет, является ли пользователь администратором.

        Args:
            tg_id: Telegram ID пользователя

        Returns:
            bool: True если пользователь администратор, иначе False

        Raises:
            SQLAlchemyError: При ошибках работы с базой данных
        """
        teacher = self.session.query(Teacher).filter_by(tg_id=tg_id).first()
        if teacher.is_admin:
            return True
        else:
            return False

    def create_group(self, group_name: str, teacher_tg_id: int) -> Group | None:
        """
        Создает новую группу и связывает ее с учителем.

        Args:
            group_name: Название группы
            teacher_tg_id: Telegram ID учителя

        Returns:
            Group: Созданный объект группы
            None: Если учитель не найден или произошла ошибка

        Raises:
            SQLAlchemyError: При ошибках работы с базой данных
        """
        try:
            teacher = self.session.query(Teacher).filter_by(tg_id=teacher_tg_id).first()

            if not teacher:
                print(f"Учитель с tg_id {teacher_tg_id} не найден")
                return None

            new_group = Group(name=group_name, teacher_id=teacher.id)
            self.session.add(new_group)
            self.session.commit()
            teacher.groups.append(new_group)
            self.session.commit()

            return new_group

        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"Ошибка при создании группы: {e}")
            return None
        finally:
            self.session.close()

