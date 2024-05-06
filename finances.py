import enum
import json
import typer
from datetime import datetime
from typing import List, Dict, Optional

import config


class FileOperations:
    """Класс для работы с файлом, хранящим данные (сохранение и выгрузка записей)"""

    def __init__(self, file_path: str):
        self.file_path = file_path

    def load_data(self) -> List[Dict]:
        """Функция загрузки записей из json файла"""

        try:
            with open(self.file_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    # Сохранение данных в json файл
    def save_data(self, data: List[Dict]):
        """Функция записи данных в json файл"""

        with open(self.file_path, 'w') as file:
            json.dump(data, file, indent=4)


class TransactionTypeEnum(enum.Enum):
    """Класс типов финансовых записей"""

    INCOME = "income"
    EXPENSE = "expense"


class FinanceManager:
    """Класс-менеджер для работы с финансами (добавление записи, получение баланса,
    редактирование записи и поиск записей)"""

    def __init__(self, file_path: str):
        self.file_operator = FileOperations(file_path=file_path)
        self.data = self.file_operator.load_data()

    def add_record(self, amount: float, category: str, date: str, description: str) -> None:
        """Функция добавляет новую запись."""

        # формируем новую запись (в зависимости от знака переданного значения определяем
        # тип финансовой операции (расход\доход))
        new_entry = {
            "amount": amount,
            "category": category,
            "date": date,
            "description": description,
            "type": TransactionTypeEnum.INCOME.value if amount >= 0 else TransactionTypeEnum.EXPENSE.value,
        }
        self.data.append(new_entry)
        self.file_operator.save_data(self.data)

    def get_balance(self) -> Dict[str, float]:
        """Функция возвращает баланс, доходы и расходы в виде словаря с соответствующими ключами."""

        # выбираем все записи по нужному нам типу и суммируем значения
        income = sum(x["amount"] for x in self.data if x["type"] == TransactionTypeEnum.INCOME.value)
        expense = sum(x["amount"] for x in self.data if x["type"] == TransactionTypeEnum.EXPENSE.value)
        return {
            "balance": income - expense,
            "income": income,
            "expense": expense,
        }

    def edit_record(self, index: int, **kwargs) -> None:
        """Функция редактирует запись."""

        if index < 0 or index >= len(self.data):
            raise IndexError("Invalid entry index.")

        record = self.data[index]

        # перебираем все переданные значения и обновляем поле, если значение не None
        for key, value in kwargs.items():
            if value is not None:
                record[key] = value
                if key == "amount":
                    record["type"] = TransactionTypeEnum.INCOME.value if value >= 0 else TransactionTypeEnum.EXPENSE.value

        self.file_operator.save_data(self.data)

    def search_records(self, **criteria) -> List[Dict]:
        """Ищет записи по критериям, переданным в качестве параметра criteria."""

        filtered = [
            x for x in self.data
            if all(criterion is None or x[key] == criterion for key, criterion in criteria.items())
        ]
        return filtered


# создаем приложение
app = typer.Typer()
# создаем менеджер для взаимодействия с записями
finance_manager = FinanceManager(config.DATA_FILE_PATH)


@app.command(help="Команда 'add' добавляет новую запись с параметрами: amount, category, date, description", name="add")
def add_entry(
        amount: float = typer.Option(..., help="Сумма транзакции"),
        category: str = typer.Option(..., help="Категория транзакции"),
        description: str = typer.Option("", help="Описание транзакции"),
        date: str = typer.Option(str(datetime.now().date()), help="YYYY-MM-DD")
):

    finance_manager.add_record(amount, category, date, description)
    typer.echo("New entry added successfully.")


@app.command(help="Команда 'balance' выводит баланс в виде полей: Balance, Incomes, Expenses", name="balance")
def get_balance():
    balance_ = finance_manager.get_balance()
    typer.echo(f"Balance: {balance_['balance']:.2f}")
    typer.echo(f"Incomes: {balance_['income']:.2f}, Expenses: {balance_['expense']:.2f}")


@app.command(
    help=""" Команда 'edit' редактирует запись об операции, принимая следующие 
параметры: index, amount, category, date, description """,
    name="edit")
def edit_entry(
    index: int = typer.Option(..., ),
    amount: Optional[float] = typer.Option(None, ),
    category: Optional[str] = typer.Option(None, ),
    date: Optional[str] = typer.Option(None, ),
    description: Optional[str] = typer.Option(None, ),
):
    try:
        finance_manager.edit_record(index, amount=amount, category=category, date=date, description=description)
        typer.echo("Entry was edited successfully.")
    except IndexError:
        typer.echo("Invalid entry index.")


@app.command(
    help=""" Команда 'search' выводит записи, найденные по переданным значениям для следующих 
параметров: category, date, max_amount, min_amount """,
    name="search")
def search_entries(
    category: Optional[str] = typer.Option(None, ),
    date: Optional[str] = typer.Option(None, ),
    max_amount: Optional[float] = typer.Option(None, ),
    min_amount: Optional[float] = typer.Option(None, ),
):
    filtered = finance_manager.search_records(
        category=category, date=date, max_amount=max_amount, min_amount=min_amount
    )

    typer.echo(f"{len(filtered)} entries were found.")
    for i, rec in enumerate(filtered):
        typer.echo(f"{i}. {rec}")


if __name__ == "__main__":
    app()
