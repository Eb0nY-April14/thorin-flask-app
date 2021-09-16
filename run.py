# This is imported from the standard Python library
import os
# We import the JSON library to enable us connect the
# data.json file we created earlier to our templates/
# views so that its contents (data) can be used by
# the about.html template/view.
import json
# Here, we are importing the Flask class. We also import
# 'render_template()' library needed to display our html
# pages & now we import 'request' library that will handle
# things like finding out what method we used & will also
# contain our form objectwhen we've posted it.
# We will import a function from Flask called 'flash' that
# will be used to display some feedback to the user.
# Sometimes, we only want to display non-permanent message
# to the user i.e something that stays only on screen until
# we refresh the page or go to a different page. These are
# called 'flash messages' in Flask.
from flask import Flask, render_template, request, flash
# We need to import env also but only if the system can
# find an 'env.py' file. if it exists, then import env.
# Once we save this, a new directory called 'pycache' is
# created & can be found amonst the files listed on the
# Sexplorer area.
if os.path.exists("env.py"):
    import env  # ignore this cos we are using env.py for the secret key

# Here, we create an instance of this Flask class & store it in a variable
# called 'app'. The 1st argument of our Flask class is the name of the
# application's module, our package. Since we are using a single module here,
# we can use "underscore underscore name underscore underscore (i.e __name__)"
# which is a built-in Python variable. Flask needs this so that it knows where
# to look for templates & static files.
app = Flask(__name__)
# We will now grab the hidden variable which we named 'SECRET KEY', to use it,
# we'll instantiate our app by writing the code directly under this comment.
app.secret_key = os.environ.get("SECRET_KEY")


# We will use the app route decorator to tell flask what URL should trigger
# the function that follows. In Python, a decorator is a way of wrapping
# functions & starts with the @ symbol also called a 'pie-notation'.
# When we try to browse to the root directory as indicated by the "/", then
# Flask triggers the index function underneath & returns the "Hello, World"
# text.
# The root decorator binds the index() function to itself so that whenever
# that root is called, the function (also known as 'view') is called so
# when we go to the "\" on the top-level of our domain, it then returns
# the template from our index() function.
# ROUTE FOR INDEX PAGE:
@app.route("/")
def index():
    # We can wrap our return text in html tags within our Python and render
    # it in the browser but only if the code isn't much but if lots of html
    # codes are involved, having to type all of that html content into our
    # Python file will complicate things so to get around this, we import
    # the render_template() function from Flask.
    # Flask expects our index.html file to be in a directory/folder called
    # 'templates' which should be at the same level as the run.py file
    return render_template("index.html")
    # return "<h1>Hello,</h1>  <h2>World</h2>" work same as the code above it


# ROUTE FOR ABOUT PAGE.
# To link up our newly created about.html page, we'll do something called
# 'routing'. This will bind that route to a view (or function) that we'll
# call 'about()'
@app.route("/about")
def about():
    data = []  # initialise an empty array called data
    # In the code after this comment block, Python is opening the
    # 'company.json' file as "r" which means "read-only" & assigns
    # the content of the file to a new variable we've just created
    # called "json_data".
    with open("data/company.json", "r") as json_data:
        # We set our empty 'data' list to equal the parsed json data
        # that we've sent through
        data = json.load(json_data)
    # 'page_title' used below is just a variable name.
    # It is a convention to always use underscore when
    # defining Python variables.
    # We can have as many arguments as we like inside
    # the render_template() function.
    # A very useful feature of using frameworks is that we can
    # actually set data on our server-side i.e our 'run.py' &
    # get it to come through/displayed on the client-side using
    # the render_template() function as done on the next line
    # and on all other views below.
    # We'll create another variable called 'company' & make our 'data'
    # list variable created on line 57 equal to it, then we'll pass the
    # newly created 'company' variable into our return statement.
    return render_template("about.html", page_title="About", company=data)


# The angled bracket used in this route decorator will pass in data from
# the URL path into our view below & we chose to call that parameter
# 'member_name'
@app.route("/about/<member_name>")
# We'll create our 'about_member()' view that will take 'member_name' from
# the line above this comment as its argument.
# Note that whenever we look at our 'about' URL & it has a name after it, that
# name will be passed into the 'about' view for example, in our own case, our
# 'about' has 'member_name' after it so 'member_name' will be passed into our
# 'about' view.
def about_member(member_name):
    # This empty object called 'member' is created to store our data
    member = {}
    with open("data/company.json", "r") as json_data:
        # 'data' is a json file so is returned as an array
        data = json.load(json_data)
        for obj in data:  # iterate through the data array
            # We are checking if the 'obj' object's url key from the jsson file
            # is equal to the member_name we passed through from the URL path.
            if obj["url"] == member_name:
                # if they do match, then we make our empty 'member' object
                # created on line 86 to equal to the 'obj' object in this
                # loop instance.
                member = obj
    # Since we've created a new html file called member.html to provide basic
    # info about each member, then we don't need this hardcoded return
    # statement below so I'll comment it out & add another piece of code that
    # is generic & can cater for whatever name we need
    # return "<h1>" + member["name"] + "</h1>"
    # Note that the 1st 'member' in the piece of code after this comment is the
    # variable name being passed through into our html file while the second
    # 'member' is the member object we created above on line 86.
    return render_template("member.html", member=member)


# ROUTE FOR CONTACT US PAGE.
# To link up our newly created contact.html page, we'll do something called
# 'routing'. This will bind that route to a view (or function) that we'll
# call 'contact()'
# To make our server/code 'i.e run.py' handle any other request other than
# the 'GET' method such as 'POST', 'PUT', 'DELETE' etc, we need to explicitly
# state that our route can accept those methods/requests. In our own case,
# it's the 'POST' method we are dealing with so we need to add 'POST' to the
# <form> tag in 'contact.html' file & within the run.py file, we need to locate
# our 'contact' route & add in another argument called 'methods' which equals
# to the list containing the 'GET' & 'POST'. Note that the list variable must
# be called 'methods' even if we only have a single method of 'POST'.
# When we submit a form, it has the form-object attached.
@app.route("/contact", methods=["GET", "POST"])
def contact():
    # Here, we'll use the 'method' of the 'request' object
    if request.method == 'POST':
        # On the next line after this comment, I'll test the if statement
        # print("Hello! Is anybody there?")
        # When we check the output of the line of code after this comment
        # in the terminal debugger, we'll see this thing called an
        # 'ImmutableMultiDict' preceeding the data that came through from
        # our form i.e my name, email address, phone no & message all being
        # passed through our 'POST' method with a status code of 200 which
        # means it works 'Ok'.
        # Since our request.form returns a dictionary, we can use standard
        # Python method of accessing the keys for that dictionary as shown
        # below.
        # By using .get(), if the value for the requested key does not exist,
        # it will display 'None' by default.
        # print(request.form.get("name"))

        # By using request.form[] alone, if the value for the requested key
        # does not exist, it will throw an 'Exception' instead of displaying
        # 'None'.
        # print(request.form["email"])
        flash("Thanks {}, we have received your message!".format(
            request.form.get("name")))
        # Here, we will now call the flash() function instead of the print
        # statements
    return render_template("contact.html", page_title="Contact")


# ROUTE FOR CAREERS PAGE.
# To link up our newly created careers.html page, we'll do something called
# 'routing'. This will bind that route to a view (or function) that we'll
# call 'careers()'
@app.route("/careers")
def careers():
    return render_template("careers.html", page_title="Careers")


# ADD EXTRA FUNCTIONALITY THAT WILL HELP TO GET OUR APPLICATION RUNNING
# We'll reference this built-in variable by saying that if name is equal
# to main (both wrapped in double underscores), then we'll run our app
# with the following arguments. We'll use the os module from the standard
# library to get the "IP" environment variable if it exist or set a default
# value if it's not found. Same goes with the 'PORT' too but we'll cast this
# as an int() & set its default to '5000' which is the common port used by
# flask. Also, setting debug to true makes debugging our code much easier
# during the development stage. The word 'main' wrapped in double underscores
# is the name of the default module in Python. Then, we'll run our app using
# the arguments we passed into the statement. We must ensure we change
# debug=True to debug=False b4 submitting our projects or else it can lead to
# security flaw. We only need it to be set to true while we are in development
# stage to debug errors in our code.
if __name__ == "__main__":
    app.run(
        host=os.environ.get("IP", "0.0.0.0"),
        port=int(os.environ.get("PORT", "5000")),
        debug=True)  # We must not have debug=True in our production app
