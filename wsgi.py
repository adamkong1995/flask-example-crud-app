from flaskr.app import app
import sys
from flaskr import key

if app.config['ENV'] == 'development':
    app.run(debug=True)
elif app.config['ENV'] == 'production':
    sys.path.append(key.PROJECT_PATH)
    from flaskr.app import app as application
