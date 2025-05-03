import sqlite3
import os
from typing import List, Dict, Optional
from cryptography.hazmat.primitives import serialization

class DatabaseManager:
    def __init__(self, db_name='chat.db'):
        # Create database directory if not exists
        os.makedirs('data', exist_ok=True)
        self.db_path = os.path.join('data', db_name)
        self.conn = sqlite3.connect(self.db_path)
        self.create_tables()
    
    def create_tables(self):
        cursor = self.conn.cursor()
        
        # Users table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            public_key TEXT NOT NULL,
            ip_address TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        # Messages table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender_id INTEGER NOT NULL,
            receiver_id INTEGER NOT NULL,
            encrypted_message TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (sender_id) REFERENCES users(id),
            FOREIGN KEY (receiver_id) REFERENCES users(id)
        )
        """)
        
        # Contacts table (optional)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            user_id INTEGER NOT NULL,
            contact_id INTEGER NOT NULL,
            PRIMARY KEY (user_id, contact_id),
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (contact_id) REFERENCES users(id)
        )
        """)
        
        self.conn.commit()

    def add_user(self, username: str, public_key: str, ip_address: str) -> bool:
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, public_key, ip_address) VALUES (?, ?, ?)",
                (username, public_key, ip_address)
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False  # Username already exists
        except Exception as e:
            print(f"Error adding user: {e}")
            return False

    def get_user(self, username: str) -> Optional[Dict]:
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT id, username, public_key, ip_address FROM users WHERE username=?",
            (username,)
        )
        row = cursor.fetchone()
        if row:
            return {
                'id': row[0],
                'username': row[1],
                'public_key': row[2],
                'ip_address': row[3]
            }
        return None

    def get_all_users(self) -> List[Dict]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, username, public_key, ip_address FROM users")
        return [{
            'id': row[0],
            'username': row[1],
            'public_key': row[2],
            'ip_address': row[3]
        } for row in cursor.fetchall()]

    def save_message(self, sender_id: int, receiver_id: int, encrypted_message: str) -> bool:
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO messages (sender_id, receiver_id, encrypted_message) VALUES (?, ?, ?)",
                (sender_id, receiver_id, encrypted_message)
            )
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error saving message: {e}")
            return False

    def get_messages(self, user1_id: int, user2_id: int, limit=100) -> List[Dict]:
        cursor = self.conn.cursor()
        cursor.execute("""
        SELECT sender_id, encrypted_message, timestamp 
        FROM messages 
        WHERE (sender_id=? AND receiver_id=?) OR (sender_id=? AND receiver_id=?)
        ORDER BY timestamp DESC
        LIMIT ?
        """, (user1_id, user2_id, user2_id, user1_id, limit))
        
        messages = []
        for row in cursor.fetchall():
            messages.append({
                'sender_id': row[0],
                'encrypted_message': row[1],
                'timestamp': row[2],
                'is_me': row[0] == user1_id
            })
        return messages[::-1]  # Return in chronological order

    def add_contact(self, user_id: int, contact_id: int) -> bool:
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO contacts (user_id, contact_id) VALUES (?, ?)",
                (user_id, contact_id)
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False  # Contact already exists
        except Exception as e:
            print(f"Error adding contact: {e}")
            return False

    def get_contacts(self, user_id: int) -> List[Dict]:
        cursor = self.conn.cursor()
        cursor.execute("""
        SELECT u.id, u.username, u.public_key, u.ip_address 
        FROM contacts c
        JOIN users u ON c.contact_id = u.id
        WHERE c.user_id = ?
        """, (user_id,))
        
        return [{
            'id': row[0],
            'username': row[1],
            'public_key': row[2],
            'ip_address': row[3]
        } for row in cursor.fetchall()]

    def __del__(self):
        if hasattr(self, 'conn'):
            self.conn.close()