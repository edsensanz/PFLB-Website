#all this file does is runs the website when you run it using terminal
#python .../main.py
#paste into terminal with the correct directory to run website
from website import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
