from datetime import date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Ledger(Base):
    __tablename__ = "ledger"

    id: Mapped[int] = mapped_column(primary_key=True)
    tx_date: Mapped[date]
    tx_code: Mapped[str]
    doc_ref: Mapped[str]
    debit: Mapped[float]
    credit: Mapped[float]

    def __repr__(self) -> str:
        fields = [
            f"id={self.id}",
            f"tx_date={self.tx_date}",
            f"tx_code={self.tx_code}",
            f"doc_ref={self.doc_ref}",
            f"debit={self.debit}",
            f"credit={self.credit}",
        ]
        return f"User({', '.join(fields)})"
