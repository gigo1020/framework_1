from sqlalchemy.orm import Session
from src.main.api.db.models.credit_table import Credit


class CreditCrudDb:
    @staticmethod
    def get_credit_by_id(db: Session, credit_id: int) -> Credit | None:
        """Возвращает кредит из базы данных по credit_id, если он существует, иначе возвращает None"""
        return db.query(Credit).filter_by(id=credit_id).first()

    @staticmethod
    def get_credit_by_account_id(db: Session, account_id: int) -> Credit | None:
        """Возвращает кредит из базы данных по account_id, если он существует, иначе возвращает None"""
        return db.query(Credit).filter_by(account_id=account_id).first()

    @staticmethod
    def create_credit(db: Session, credit: Credit) -> Credit | None:
        """Создает новый кредит в базе данных"""
        db.add(credit)
        db.commit()
        db.refresh(credit)
        return credit

    @staticmethod
    def delete_credit(db: Session, credit_id: int) -> None:
        """Удаляет кредит из базы данных по его credit_id"""
        credit = db.query(Credit).filter_by(id=credit_id).first()
        if credit:
            db.delete(credit)
            db.commit()

    @staticmethod
    def account_credits_count(db: Session, account_id: int) -> int:
        """Считает количество кредитов в БД, связанных с указанным account_id"""
        return db.query(Credit).filter_by(account_id=account_id).count()
