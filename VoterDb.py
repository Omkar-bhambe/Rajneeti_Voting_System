import pymysql

class VoterSystemDatabase:

    def __init__(self):
        self.conn = pymysql.connect(
            host='localhost',
            user='root',
            password='Samruddhi@2004',
            database='voter_system'
        )
        self.cursor = self.conn.cursor()

    def admin_register(self, email_id, admin_username, password):
        # Use parameterized query to prevent SQL injection
        self.cursor.execute("SELECT * FROM admins WHERE email_id = %s", (email_id,))
        admin_data = self.cursor.fetchall()

        # print(admin_data)

        if len(admin_data) > 0:
            return 0
        else:
            self.cursor.execute(
                "INSERT INTO admins (email_id, admin_username, password) VALUES (%s, %s, %s)",
                (email_id, admin_username, password)
            )
            self.conn.commit()
            return 1

    def voter_register(self, email_id, password, stud_id):
        self.cursor.execute("SELECT * FROM voters WHERE email_id = %s", (email_id,))
        voter_data = self.cursor.fetchall()

        # print(voter_data)

        if len(voter_data) > 0:
            return 0
        else:
            self.cursor.execute(
                "INSERT INTO voters (email_id, password, stud_id) VALUES (%s, %s, %s)",
                (email_id, password, stud_id)
            )
            self.conn.commit()
            return 1

    def check_admin(self, email_id, password):
        self.cursor.execute("SELECT * FROM admins WHERE email_id = %s", (email_id,))
        admin_data = self.cursor.fetchall()

        # print(admin_data[0][-1])
        if len(admin_data) > 0:
            if password == admin_data[0][-1]:
                return 1
            else:
                return -2
        else:
            return 0

        # print(admin_data[0][-1])

    def check_voter(self, email_id, voter_password):
        self.cursor.execute("SELECT * FROM voters WHERE email_id = %s", (email_id,))
        voter_data = self.cursor.fetchall()

        # print(voter_data[0][-2])

        if len(voter_data) > 0:
            if voter_password == voter_data[0][-2]:
                return 1
            else:
                return -1
        else:
            return 0


    def get_candidates(self):
        self.cursor.execute("SELECT candidate_name FROM results")
        candidates = self.cursor.fetchall()

        return [candidate[0] for candidate in candidates]

    def add_candidate(self, candidate_name):
        self.cursor.execute(f"INSERT INTO results (candidate_name) VALUES (%s)", (candidate_name,))
        self.conn.commit()

    def cast_vote(self, candidate_name):
        self.cursor.execute(f"UPDATE results SET vote_count = vote_count + 1 WHERE candidate_name = %s", (candidate_name,))
        self.conn.commit()

    def get_results(self):

        self.cursor.execute("SELECT candidate_name, vote_count FROM results")
        return self.cursor.fetchall()


    def remove_candidate(self):

        self.cursor.execute("DELETE FROM results")
        self.conn.commit()


    def update_admin_credentials(self, admin_username, new_password):

        self.cursor.execute("SELECT * FROM admins WHERE admin_username = %s", (admin_username,))
        admin_data = self.cursor.fetchone()

        if admin_data:

            self.cursor.execute(
                "UPDATE admins SET password = %s WHERE admin_username = %s",
                (new_password, admin_username)
            )

            self.conn.commit()

            return True

        else:

            return False


    def update_voter_password(self, stud_id, new_password):

        self.cursor.execute("SELECT * FROM voters WHERE stud_id = %s", (stud_id,))
        voter_data = self.cursor.fetchone()

        if voter_data:
            self.cursor.execute(
                "UPDATE voters SET password = %s WHERE stud_id = %s",
                (new_password, stud_id)
            )
            self.conn.commit()

            return True

        else:

            return False

    def get_voters(self):
        self.cursor.execute("SELECT stud_id, email_id FROM voters")
        return self.cursor.fetchall()

        # print(voter_data[0][-1])

    def save_conversation(self, user_message, bot_response):
        self.cursor.execute("INSERT INTO chat_bot_prompts (user_message, bot_response) VALUES (%S, %S)",
                            (user_message, bot_response)
                            )
        self.conn.commit()





# db = VoterSystemDatabase()
# db.update_admin_credentials('dummy1', '1234')

