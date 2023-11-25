import sqlite3
from datetime import datetime, timedelta

from app.logs import logging


class Users:
    def __init__(self, db_path="app/db/users.db"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    telegram_id INTEGER PRIMARY KEY, 
                    wallet_count INTEGER DEFAULT 1,
                    time_wait TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    free_run INTEGER DEFAULT 1, 
                    current_balance FLOAT DEFAULT 0.0
                )
            """)
            self.conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Error creating table: {e}")

    def _update_time_wait(self, user_id):
        formatted_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            self.cursor.execute("""
                UPDATE users
                SET time_wait = ?
                WHERE telegram_id = ?
            """, (formatted_date, user_id))
            self.conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Error updating time_wait: {e}")

    def set_max_wallets_count(self, user_id, wallet_count):
        try:
            self.cursor.execute("""
                INSERT OR IGNORE INTO users (telegram_id) VALUES (?)
            """, (user_id,))
            self.cursor.execute("""
                UPDATE users SET wallet_count = ? WHERE telegram_id = ?
            """, (wallet_count, user_id))
            self.conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Error setting max wallets count: {e}")

    def change_current_balance(self, user_id, money_to_add):
        try:
            self.cursor.execute("""
                INSERT OR IGNORE INTO users (telegram_id) VALUES (?)
            """, (user_id,))
            self.cursor.execute("""
                UPDATE users SET current_balance = ? WHERE telegram_id = ?
            """, (money_to_add, user_id))
            self.conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Error change_current_balance: {e}")

    def is_free_run(self, user_id):
        try:
            self.cursor.execute("""
                SELECT free_run FROM users WHERE telegram_id = ?
            """, (user_id,))
            result = self.cursor.fetchone()
            self._update_time_wait(user_id)  # Обновляем time_wait
            print(result)
            return result[0] if result else None
        except sqlite3.Error as e:
            logging.error(f"Error fetching gree_run: {e}")
            return None


    def get_max_wallets(self, user_id):
        try:
            self.cursor.execute("""
                SELECT wallet_count FROM users WHERE telegram_id = ?
            """, (user_id,))
            result = self.cursor.fetchone()
            self._update_time_wait(user_id)  # Обновляем time_wait
            return result[0] if result else None
        except sqlite3.Error as e:
            logging.error(f"Error fetching max wallets: {e}")
            return None

    def get_time_wait(self, user_id):
        try:
            self.cursor.execute("""
                SELECT time_wait FROM users WHERE telegram_id = ?
            """, (user_id,))
            result = self.cursor.fetchone()
            return datetime.strptime(result[0], '%Y-%m-%d %H:%M:%S') if result else None
        except sqlite3.Error as e:
            logging.error(f"Error fetching time wait: {e}")
            return None

    def add_user(self, user_id, time_wait, wallet_count):
        try:
            self.cursor.execute("""
                INSERT OR IGNORE INTO users (telegram_id, wallet_count, time_wait)
                VALUES (?, ?, ?)
            """, (user_id, wallet_count, time_wait))
            self.conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Error adding user: {e}")


    def get_current_balance(self, user_id):
        try:
            self.cursor.execute("""
                SELECT current_balance FROM users WHERE telegram_id = ?
            """, (user_id,))
            result = self.cursor.fetchone()
            self._update_time_wait(user_id)  # Обновляем time_wait
            return result[0] if result else None
        except sqlite3.Error as e:
            logging.error(f"Error fetching current_balance: {e}")
            return None

    def update_balance(self, user_id, to_add):
        balance = self.get_current_balance(user_id)
        new_balance = balance + to_add
        try:
            self.cursor.execute("""
                UPDATE users
                SET current_balance = ?
                WHERE telegram_id = ?
            """, (new_balance, user_id))
            self._update_time_wait(user_id)  # Обновляем time_wait
            self.conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Error setting request update_balance: {e}")

    def set_false_free_run(self, user_id):
        try:
            self.cursor.execute("""
                UPDATE users
                SET free_run = ?
                WHERE telegram_id = ?
            """, (0, user_id))
            self._update_time_wait(user_id)  # Обновляем time_wait
            self.conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Error setting request count and date: {e}")

    def get_all_users(self):
        try:
            self.cursor.execute("SELECT telegram_id FROM users")
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            logging.error(f"Error fetching all users: {e}")
            return []

    def get_active_users_count(self, days):
        date_limit = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d %H:%M:%S')
        try:
            self.cursor.execute("""
                SELECT COUNT(telegram_id) FROM users WHERE time_wait > ?
            """, (date_limit,))
            return self.cursor.fetchone()[0]
        except sqlite3.Error as e:
            logging.error(f"Error fetching active users: {e}")
            return 0

    def get_all_users_by_balance(self):
        try:
            self.cursor.execute("SELECT telegram_id, current_balance FROM users")
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            logging.error(f"Error fetching users: {e}")
            return []




    def close(self):
        self.conn.close()
