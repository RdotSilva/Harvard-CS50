import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    if request.method == "GET":
        userId = session["user_id"]

        # Users balance
        userMoney = db.execute("SELECT cash FROM users WHERE id = :id", id=userId)

        userCash = userMoney[0].get("cash")

        # Query database for all transactions by users
        stocks = db.execute(
            "SELECT symbol, SUM(shares) as total_shares FROM transactions WHERE user_id = :userId GROUP BY symbol HAVING total_shares > 0", userId=userId)
        print(stocks)

        # Get current price of each stock
        currentStockPrices = {}

        # User to store the value of user cash + current stock price value of shares
        cashWithStocks = userCash

        for stock in stocks:
            currentStockPrices[stock["symbol"]] = lookup(stock["symbol"])
            cashWithStocks += (currentStockPrices[stock["symbol"]]["price"] * stock["total_shares"])

        return render_template("index.html", stocks=stocks, currentStockPrices=currentStockPrices, userCash=userCash, cashWithStocks=cashWithStocks)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure symbol is submitted
        if not request.form.get("symbol"):
            return apology("must enter stock symbol", 400)

        if not request.form.get("shares").isdigit():
            return apology("share must be a number", 400)

        # Ensure positive share number is submitted
        if int(request.form.get("shares")) <= 0:
            return apology("share number must be greater than 0", 400)

        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        # Lookup stock
        quote = lookup(symbol)

        # If symbol is valid and stock exists
        if (quote):
            price = quote.get("price")
            userId = session["user_id"]

            # Total cost of stock price*shares
            totalCost = price * float(shares)

            # Users balance
            userMoney = db.execute("SELECT cash FROM users WHERE id = :id", id=userId)

            # Users name
            username = db.execute("SELECT username FROM users WHERE id = :id", id=userId)

            userCash = userMoney[0].get("cash")
            user = username[0].get("username")

            # If user has enough money to buy stock
            if userCash >= totalCost:
                # Insert transaction into database
                db.execute("INSERT INTO transactions(user_id, symbol, price, shares) VALUES(:user_id, :symbol, :price, :shares)",
                           user_id=userId, symbol=symbol, price=price, shares=shares)

                # Subtract purchase price from users total available cash
                db.execute("UPDATE users SET cash = (cash - :totalCost) WHERE id = :id", id=userId, totalCost=totalCost)

                return redirect('/')

            # If user doesnt have enough money render apology
            else:
                return apology("not enough funds to buy stock", 400)
        else:
            return apology("invalid stock symbol", 400)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("buy.html")


@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""
    username = request.args.get("username")

    checkNames = db.execute("SELECT username FROM users WHERE username = :username", username=username)

    if len(checkNames) == 0:
        return jsonify(True)
    else:
        return jsonify(False)


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    if request.method == "GET":
        userId = session["user_id"]

        # Users transaction history
        transactions = db.execute("SELECT * FROM transactions WHERE user_id = :id ORDER BY datetime ASC", id=userId)
        print(transactions)

        return render_template("history.html", transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure symbol is submitted
        if not request.form.get("symbol"):
            return apology("must enter stock symbol", 400)

        # Lookup stock
        quote = lookup(request.form.get("symbol"))

        if (quote):
            # Render new page with stock quote
            return render_template("quoted.html", quote=quote)
        else:
            return apology("invalid stock symbol", 400)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        hashed = generate_password_hash(password)

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure password was submitted
        elif not request.form.get("confirmation"):
            return apology("must confirm password", 400)

        # Check if passwords match
        elif password != confirmation:
            return apology("passwords must match", 400)

        # Check if username doesnt already exist

        checkNames = db.execute("SELECT username FROM users WHERE username = :username", username=username)
        if len(checkNames) != 0:
            return apology("username is taken", 400)

        # Insert user data into database
        db.execute(
            "INSERT INTO users(username, hash) VALUES(:username, :hash)", username=username, hash=hashed)

        # Log user in after registration
        session.get("user_id")

        return redirect("/")
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure symbol is submitted
        if not request.form.get("symbol"):
            return apology("must enter stock symbol", 400)
        # Ensure positive share number is submitted
        if int(request.form.get("shares")) <= 0:
            return apology("share number must be greater than 0", 400)

        symbol = request.form.get("symbol")
        shares = request.form.get("shares")
        userId = session["user_id"]

        # Lookup stock
        quote = lookup(symbol)

        if quote == None:
            return apology("invalid stock symbol", 400)

        # Query database for stock to check if we have enough shares
        stock = db.execute(
            "SELECT symbol, SUM(shares) as total_shares FROM transactions WHERE user_id = :userId AND symbol = :symbol", userId=userId, symbol=symbol)

        if stock[0]["total_shares"] < int(shares):
            return apology("not enough shares to sell", 400)

        price = quote.get("price")
        userId = session["user_id"]

        # Total cost of stock price*shares
        totalCost = price * float(shares)

        # Users balance
        userMoney = db.execute("SELECT cash FROM users WHERE id = :id", id=userId)

        # Users name
        username = db.execute("SELECT username FROM users WHERE id = :id", id=userId)

        userCash = userMoney[0].get("cash")
        user = username[0].get("username")

        shares = int(shares)

        # Insert transaction into database
        db.execute("INSERT INTO transactions(user_id, symbol, price, shares) VALUES(:user_id, :symbol, :price, :shares)",
                   user_id=userId, symbol=symbol, price=price, shares=-shares)

        # Subtract purchase price from users total available cash
        db.execute("UPDATE users SET cash = (cash + :totalCost) WHERE id = :id", id=userId, totalCost=totalCost)

        return redirect('/')

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        userId = session["user_id"]

        # Get list of stocks that user owns
        stocks = db.execute(
            "SELECT symbol, SUM(shares) as total_shares FROM transactions WHERE user_id = :userId GROUP BY symbol HAVING total_shares > 0", userId=userId)
        print(stocks)
        return render_template("sell.html", stocks=stocks)


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    # Add money to account

    if request.method == "POST":
        userId = session["user_id"]
        deposit = request.form.get("dollars")

        if not request.form.get("dollars"):
            return apology("enter dollar amount to add", 400)

        try:
            dollarAmount = float(request.form.get("dollars"))
        except ValueError:
            return apology("dollar amount must be valid number", 400)

        if dollarAmount <= 0:
            return apology("dollar amount must be positive number", 400)

        # Users balance
        userMoney = db.execute("SELECT cash FROM users WHERE id = :id", id=userId)

        userCash = userMoney[0].get("cash")

        # Add new amount into users cash
        db.execute("UPDATE users SET cash = (cash + :deposit) WHERE id = :id", id=userId, deposit=deposit)

        return redirect("/")
    else:
        return render_template("add.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
