import sqlite3 as sql
from werkzeug.security import generate_password_hash, check_password_hash


class databaseHandler:
    def __init__(self, dbName = 'appdata.db'):
        self.dbName = dbName

    def connect(self):
        return sql.connect(self.dbName)
    
    def createTable(self):
        with self.connect() as conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS  users(
                         userID INTEGER PRIMARY KEY AUTOINCREMENT,
                         username TEXT UNIQUE NOT NULL CHECK(length(username) > 2),
                         password TEXT NOT NULL CHECK(length(password) > 7)
                         );''')

            conn.execute('''CREATE TABLE IF NOT EXISTS tasks(
                         taskID INTEGER PRIMARY KEY AUTOINCREMENT,
                         userID INTEGER NOT NULL,
                         taskName TEXT NOT NULL CHECK(length(taskName) > 2),
                         taskDescription TEXT NOT NULL,
                         status TEXT DEFAULT 'incomplete' CHECK(status IN ('incomplete', 'complete')),
                         created TEXT DEFAULT CURRENT_TIMESTAMP,
                         FOREIGN KEY (userID) REFERENCES users(userID) ON DELETE CASCADE
                         )''')


    def createUser(self, username, password):
        try:
            hashedPassword = generate_password_hash(password)
            with self.connect() as conn:
                conn.execute('INSERT INTO users(username, password) VALUES(?, ?)', (username, hashedPassword))
                conn.commit()
            return True, None
    
        except sql.IntegrityError as error:
            print(error)
            if 'UNIQUE' in str(error):
                return False, 'unique-error'
            else:
                return False, 'integrity-error'
        
        except Exception as error:
            print(error)
            return False , 'unknown-error'
        

    def authoriseUser(self, username, password):
        try:
            with self.connect() as conn:
                results = conn.execute('SELECT password, userID FROM users WHERE username = ?', (username,))
                storedHash, userID = results.fetchone()
                if check_password_hash(storedHash, password):
                    return True, userID
                else:
                    return False, None
                
        except:
            return False
    

    def createTask(self, taskName, description, userID):
        try:
            with self.connect() as conn:
                conn.execute('''INSERT INTO tasks
                             (taskName, taskDescription, userID)
                             VALUES
                             (?,?,?) ''', (taskName, description, userID))
                conn.commit()
            return True, None
        except:
            return False, 'unknown-error'
        
    def fetchAllTask(self, userID):
        try:
            with self.connect() as conn:
                results = conn.execute('''SELECT taskID, taskName, taskDescription, status, created
                             FROM tasks
                             WHERE userID = ?''', (userID, ))
                tasks = results.fetchall()
                if len(tasks) > 0:
                    return True, tasks
                
                return True, None

        except:
            return False, None
        
    def deleteTask(self, taskID, userID):
        try:
            with self.connect() as conn:
                conn.execute('DELETE FROM tasks WHERE taskID =? AND userID = ?', (taskID, userID))
                conn.commit()

                return True

        except:
            return False
        
    def updateStatus(self, taskID, userID):
        try:
            with self.connect() as conn:
                conn.execute('''UPDATE tasks 
                                SET status = CASE status 
                                    WHEN "complete" THEN "incomplete"
                                    ELSE "complete"
                                END
                                WHERE taskID = ? and userID = ?;''', (taskID, userID))
                conn.commit()
                return True
        
        except Exception as error:
            print(error)
            return False
