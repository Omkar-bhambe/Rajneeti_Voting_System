from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify

from VoterDb import VoterSystemDatabase


app = Flask(__name__)
app.secret_key = 'UPDATE_SECRET_KEY'

db = VoterSystemDatabase()

# Admin registration route
@app.route('/admin/register', methods=['GET', 'POST'])
def admin_register():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        # confirm_password = PasswordField('confirm password', validators=[EqualTo('password', message='Password and Confirm Password are not matching')])

        result = db.admin_register(email, username, password)

        if result == 1:

            flash('Admin registration successful!', 'success')
            return redirect(url_for('admin_login'))
        else:

            flash('Admin already exists! Please go to login', 'error')
            return redirect(url_for('admin_login'))

    return render_template('admin_register.html')

# Admin login route
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        result = db.check_admin(email, password)
        if result == 1:

            session['admin'] = email
            flash('Admin login successful!', 'success')

            return redirect(url_for('admin'))
        else:

            flash('Invalid credentials!', 'error')

    return render_template('admin_login.html')

# Admin dashboard for registering candidates
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if 'admin' not in session:

        flash('Please login as admin first!', 'error')
        return redirect(url_for('admin_login'))

    if request.method == 'POST':
        candidate_name = request.form['candidate_name']

        if candidate_name and candidate_name not in db.get_candidates():
            db.add_candidate(candidate_name)
            flash('Candidate registered successfully!', 'success')

        else:
            flash('Candidate name cannot be empty or already exists!', 'error')

    candidates = db.get_candidates()
    return render_template('admin.html', candidates=candidates)

@app.route('/admin/delete_all', methods = ['POST'])
def delete_all_candidates():
    if 'admin' not in session:
        flash("Please login as admin first", 'warning')
        return redirect(url_for('admin_login'))

    db.remove_candidate()
    flash('New session started successfully', 'success')
    return redirect(url_for('admin'))

# Voter registration route
@app.route('/voter/register', methods=['GET', 'POST'])
def voter_register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        stud_id = request.form['stud_id']

        result = db.voter_register(email, password, stud_id)
        if result == 1:

            flash('Voter registration successful!', 'success')

            return redirect(url_for('voter_login'))

        else:

            flash('Voter already exists!', 'error')

    return render_template('voter_register.html')

# Voter login route
@app.route('/voter/login', methods=['GET', 'POST'])
def voter_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        results = db.check_voter(email, password)

        if results == 1:

            session['voter'] = email
            flash('Voter login successful. You can now cast your votes !!!', 'success')

            return redirect(url_for('vote'))

        elif results == -2:

            flash('Invalid Credentials !', 'error')
            return redirect(url_for('voter_login'))

        else:

            flash("Invalid credentials or voter doesn't exist please register as a voter first.", 'error')

            return redirect(url_for('voter_login'))

    return render_template('voter_login.html')

# Voter route to cast a vote
@app.route('/vote', methods=['GET', 'POST'])
def vote():

    if 'voter' not in session:
        flash('Please login as a voter first!', 'error')
        return redirect(url_for('voter_login'))

    candidates = db.get_candidates()

    if request.method == 'POST':
        chosen_candidate = request.form.get('candidate')
        if chosen_candidate:
            db.cast_vote(chosen_candidate)
            flash(f'Vote cast for {chosen_candidate}!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Please select a candidate to vote!', 'error')

    return render_template('vote.html', candidates=candidates)

# Results route to display voting results
@app.route('/results')
def results():

    result_data = db.get_results()

    vote_results = {candidate: votes for candidate, votes in result_data}

    return render_template('result.html', votes=vote_results)
    print(vote_results)

# Home route
@app.route('/')
def home():
    return render_template('homes.html')

# Logout route
@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('home'))


@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot():

    if request.method == 'POST':

        stud_id = request.form.get('username')
        new_password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if new_password != confirm_password:
            flash("Password doesn't match.", 'error')
            return redirect(url_for('forgot'))

        result = db.update_voter_password(stud_id, new_password)

        if result:

            flash('Password Updated Successfully', 'success')
            return redirect(url_for('voter_login'))

        else:

            flash('Student not Found please contact your college', 'warning')
            return redirect(url_for('forgot'))

    return render_template('forgot.html')

@app.route('/admin/voters', methods=['GET'])
def view_voters():
    if 'admin' not in session:
        flash('please login as a admin first', 'error')
        return redirect(url_for('admin_login'))

    voters = db.get_voters()

    return render_template('view_voters.html', voters=voters)

@app.route('/chatbot', methods=['POST'])
def chatbot():
    user_message = request.json.get('message')
    bot_response = get_bot_response(user_message)
    db.save_conversation(user_message, bot_response)
    return jsonify({'response': bot_response})

def get_bot_response(user_message):
    lower_message = user_message.lower()

    if 'vote' in lower_message:
        return 'To cast your vote, click the "Vote" button next to your preferred candidate.'

    elif 'logout' in lower_message:
        return 'Click on "logout" button at the bottom of the page to log out.'

    else:
        "I'm not sure what your saying please ask me about voting and logout only !!!"

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)

