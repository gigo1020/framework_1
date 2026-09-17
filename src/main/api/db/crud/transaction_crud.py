from sqlalchemy.orm import Session
from src.main.api.db.models.transaction_table import Transaction


class TransactionCrudDb:
    @staticmethod
    def get_transaction_by_id(db: Session, transaction_id: int) -> Transaction | None:
        """Возвращает транзакцию из базы данных по transaction_id, если она существует, иначе возвращает None"""
        return db.query(Transaction).filter_by(id=transaction_id).first()

    @staticmethod
    def get_latest_transaction_by_from_account_id(db: Session, from_account_id: int) -> Transaction | None:
        """Возвращает самую недавнюю транзакцию из базы данных по from_account_id, если она существует, иначе возвращает None"""
        return db.query(Transaction).filter_by(from_account_id=from_account_id).order_by(
            Transaction.created_at.desc()).first()

    @staticmethod
    def create_transaction(db: Session, transaction: Transaction) -> Transaction | None:
        """Создает новую транзакцию в базе данных"""
        db.add(transaction)
        db.commit()
        db.refresh(transaction)
        return transaction

    @staticmethod
    def delete_transaction(db: Session, transaction_id: int) -> None:
        """Удаляет транзакцию из базы данных по ее transaction_id"""
        transaction = db.query(Transaction).filter_by(id=transaction_id).first()
        if transaction:
            db.delete(transaction)
            db.commit()

    @staticmethod
    def transactions_count(db: Session, from_account_id: int) -> int:
        """Считает количество транзакций в БД, связанных с указанным from_account_id"""
        return db.query(Transaction).filter_by(from_account_id=from_account_id).count()
