# SQLAlchemy Datatabase Uri
#export SQLALCHEMY_DATABASE_URI='postgresql://postgres:kitten@localhost:5432/fsnd'
export DATABASE_URL=postgres://postgres:kitten@localhost:5432/fsnd
export ITEMS_PER_PAGE=10

# Flask configuration
export FLASK_APP=app.py
#export FLASK_ENV=development
export FLASK_RUN_PORT=8080

# Configurations gotten from the account created on Auth0
export AUTH0_DOMAIN=fsnd-shruti.us.auth0.com
export ALGORITHMS=RS256
export API_AUDIENCE=capstone

export AUTH0_CLIENT_ID=o8gLw5IA6cttFLhFJxLINVGoQnohcmqX
export AUTH0_CALLBACK_URL=https://127.0.0.1:8080/login-results
#export AUTH0_CALLBACK_URL=https://fsnd-capstone-cynepton.herokuapp.com/ 