# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sqlite3

class Database:
    def __init__(self):
        self.connection = None

    def get_connection(self):
        if self.connection is None:
            self.connection = sqlite3.connect('db/users.db')
        return self.connection

    def disconnect(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None


    def get_user(self, username):
        cursor = self.get_connection().cursor()
        # Injection sql
        # Sinon essayer de faire l'injection avec le query bien fait mais que le char est %
        query = "select * from users where username = '" + username + "'"
        try :
            users = cursor.execute(query).fetchall()
        except sqlite3.OperationalError:
            # Prevent errors from SQL
            cursor.close()
            return []

        cursor.close()
        return [user[1] for user in users]

    def is_valid_password(self, username, password):
        # Pas d'injection SQL ici
        cursor = self.get_connection().cursor()
        query = 'select * from users where username = ? and password = ?'
        cursor.execute(query, (username, password))
        user = cursor.fetchall()
        cursor.close()
    
        return len(user) != 0
