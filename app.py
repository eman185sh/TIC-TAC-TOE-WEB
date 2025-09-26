from flask import Flask, render_template_string, request, redirect, session, url_for

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # غيرها لسر قوي

TEMPLATE = """
<!doctype html>
<title>Tic Tac Toe</title>
<h2>Tic Tac Toe</h2>
<p>Current Player: {{ current_player }}</p>
<table style="border-collapse: collapse;">
  {% for i in range(3) %}
  <tr>
    {% for j in range(3) %}
    <td style="border: 1px solid black; width: 60px; height: 60px; text-align: center; font-size: 24px;">
      {% if board[i][j] == ' ' and not winner %}
        <a href="{{ url_for('move', row=i, col=j) }}" style="text-decoration:none; display:block; width:100%; height:100%; color:black;">&nbsp;</a>
      {% else %}
        {{ board[i][j] }}
      {% endif %}
    </td>
    {% endfor %}
  </tr>
  {% endfor %}
</table>

{% if winner %}
  <h3>{{ winner_message }}</h3>
  <a href="{{ url_for('reset') }}">Restart Game</a>
{% elif tie %}
  <h3>It's a tie!</h3>
  <a href="{{ url_for('reset') }}">Restart Game</a>
{% endif %}
"""

def check_winner(board, player):
    for row in board:
        if all(s == player for s in row):
            return True
    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)):
        return True
    if all(board[i][2 - i] == player for i in range(3)):
        return True
    return False

def is_board_full(board):
    return all(cell != " " for row in board for cell in row)

@app.route('/')
def index():
    if 'board' not in session:
        session['board'] = [[' ' for _ in range(3)] for _ in range(3)]
        session['current_player'] = 'X'
        session['winner'] = None
        session['tie'] = False

    board = session['board']
    current_player = session['current_player']
    winner = session.get('winner')
    tie = session.get('tie', False)

    winner_message = None
    if winner:
        winner_message = f"Player {winner} wins!"

    return render_template_string(TEMPLATE, board=board, current_player=current_player, winner=winner, tie=tie, winner_message=winner_message)

@app.route('/move/<int:row>/<int:col>')
def move(row, col):
    board = session.get('board')
    current_player = session.get('current_player')
    winner = session.get('winner')
    tie = session.get('tie', False)

    if winner or tie:
        return redirect(url_for('index'))

    if board[row][col] == ' ':
        board[row][col] = current_player
        if check_winner(board, current_player):
            session['winner'] = current_player
        elif is_board_full(board):
            session['tie'] = True
        else:
            session['current_player'] = 'O' if current_player == 'X' else 'X'
        session['board'] = board

    return redirect(url_for('index'))

@app.route('/reset')
def reset():
    session.pop('board', None)
    session.pop('current_player', None)
    session.pop('winner', None)
    session.pop('tie', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
