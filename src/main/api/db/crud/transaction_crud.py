

from sqlalchemy.orm import Session
from src.main.api.db.models.transaction_table import Transaction

class TransactionCrudDb:
    @staticmethod
    def get_transaction_by_id(db: Session, transaction_id: int) -> Transaction | None:
        return db.query(Transaction).filter_by(id=transaction_id).first()

    @staticmethod
    def get_latest_transaction_by_from_account_id(db: Session, from_account_id: int) -> Transaction | None:
        return db.query(Transaction).filter_by(from_account_id=from_account_id).order_by(Transaction.created_at.desc()).first()

    @staticmethod
    def create_transaction(db: Session, transaction: Transaction) -> Transaction | None:
        db.add(transaction)
        db.commit()
        db.refresh(transaction)
        return transaction

    @staticmethod
    def delete_transaction(db: Session, transaction_id: int) -> None:
        transaction = db.query(Transaction).filter_by(id=transaction_id).first()
        if transaction:
            db.delete(transaction)
            db.commit()