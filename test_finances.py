import json
import unittest
from unittest.mock import patch, mock_open
from finances import FileOperations
from unittest import TestCase
from finances import FinanceManager, TransactionTypeEnum
import pytest
from typer.testing import CliRunner
from finances import app


# Тесты для FileOperations

class TestFileOperations(unittest.TestCase):
    @patch("builtins.open", new_callable=mock_open, read_data='[{"amount": 100, "category": "Salary"}]')
    def test_load_data(self, mock_file):
        file_ops = FileOperations("test.json")
        data = file_ops.load_data()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["category"], "Salary")

    @patch("builtins.open", new_callable=mock_open)
    def test_save_data(self, mock_file):
        file_ops = FileOperations("test.json")
        data = [{"amount": 100, "category": "Salary"}]
        file_ops.save_data(data)

        # Убедимся, что файл открыт на запись
        mock_file.assert_called_once_with("test.json", 'w')

        # Проверяем, что `write` был вызван и не пустой
        self.assertGreater(len(mock_file().write.call_args_list), 0, "No write calls were made")

        # Собираем все вызовы `write` в одну строку
        written_data = "".join(
            call[0][0] if isinstance(call[0], tuple) else call[0]
            for call in mock_file().write.call_args_list
        )

        # Ожидаемое содержимое файла в виде JSON
        expected_data = json.dumps(data, indent=4)

        # Сравниваем записанные данные с ожидаемыми
        self.assertEqual(written_data, expected_data)


# Тесты для FinanceManager

class TestFinanceManager(TestCase):
    @patch("finances.FileOperations.load_data", return_value=[])
    @patch("finances.FileOperations.save_data")
    def test_add_record(self, mock_save_data, mock_load_data):
        manager = FinanceManager("test.json")
        manager.add_record(100, "Salary", "2023-12-01", "Main salary")

        # Проверяем, что запись была добавлена
        self.assertEqual(len(manager.data), 1)
        self.assertEqual(manager.data[0]["category"], "Salary")

        # Проверяем, что данные были сохранены
        mock_save_data.assert_called_once()

    @patch("finances.FileOperations.load_data", return_value=[
        {"amount": 100, "category": "Salary", "type": TransactionTypeEnum.INCOME.value},
        {"amount": 50, "category": "Food", "type": TransactionTypeEnum.EXPENSE.value},
    ])
    def test_get_balance(self, mock_load_data):
        manager = FinanceManager("test.json")
        balance = manager.get_balance()

        self.assertEqual(balance["balance"], 50)
        self.assertEqual(balance["income"], 100)
        self.assertEqual(balance["expense"], 50)


runner = CliRunner()

# Тесты для Команд CLI


@pytest.fixture
def cli_runner():
    return runner


def test_add_entry(cli_runner):
    result = cli_runner.invoke(
        app, ["add", "--amount", "100", "--category", "Salary", "--description", "Main salary"]
    )
    assert result.exit_code == 0
    assert "New entry added successfully" in result.output


def test_balance(cli_runner):
    result = cli_runner.invoke(app, ["balance"])
    assert result.exit_code == 0
    assert "Balance" in result.output


def test_edit_entry(cli_runner):
    result = cli_runner.invoke(
        app, ["edit", "--index", "0", "--amount", "200"]
    )
    assert result.exit_code == 0
    assert "Entry was edited successfully" in result.output


def test_search_entries(cli_runner):
    result = cli_runner.invoke(
        app, ["search", "--category", "Salary"]
    )
    assert result.exit_code == 0
    assert "entries were found" in result.output
