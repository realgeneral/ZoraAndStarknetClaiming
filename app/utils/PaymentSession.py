import sqlite3
from datetime import datetime
from app.logs import logging


class PaymentSession:
    def __init__(self, db_path="app/db/payment_sessions.db"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS payment_sessions (
                    uniq_id TEXT,
                    wallet_address TEXT,
                    private_key TEXT,
                    mnemonic_phrase TEXT,
                    network TEXT,
                    telegram_id INTEGER,
                    deposit_amount FLOAT,
                    deposit_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            self.conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Error creating table: {e}")

    def add_session(self, uniq_id, wallet_address, private_key, mnemonic_phrase, network, telegram_id, deposit_amount,
                    deposit_time=None):
        if deposit_time is None:
            deposit_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        try:
            self.cursor.execute("""
                INSERT INTO payment_sessions (uniq_id, wallet_address, private_key, mnemonic_phrase, network, telegram_id, deposit_amount, deposit_time)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (uniq_id, wallet_address, private_key, mnemonic_phrase,network, telegram_id, deposit_amount, deposit_time))
            self.conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Error adding session: {e}")

    def close(self):
        self.conn.close()

# Если вы хотите создать базу данных сразу же после запуска этого кода,
# просто создайте экземпляр этого класса:
# session = PaymentSessions()
