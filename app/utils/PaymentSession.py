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

    def stop_session(self, telegram_id):
        try:
            self.cursor.execute("""
                UPDATE payment_sessions
                SET wallet_address = NULL,
                    private_key = NULL,
                    mnemonic_phrase = NULL,
                    network = NULL,
                    deposit_amount = 0,
                    deposit_time = NULL
                WHERE telegram_id = ?
            """, (telegram_id,))
            self.conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Error updating data for telegram_id {telegram_id}: {e}")

    def close(self):
        self.conn.close()


