from flask import Flask
import icalendar
from jinja2 import Environment, FileSystemLoader

app = Flask(__name__)

@app.route('/templates')
def hello():

    # Load the Jinja environment and template
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('template.html')

    # Context data to pass into the template
    context = {
        'title': 'My Shopping List',
        'items': ['Milk', 'Eggs', 'Bread']
    }

    # Render the template with context and return it as the response
    output = template.render(context)
    return output  # Manually rendered HTML from Jinja

if __name__ == "__main__":
    app.run(debug=True)

