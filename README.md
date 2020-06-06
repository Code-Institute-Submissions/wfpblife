# WFPB LIFE

### Data Driven Milestone Project

This project comes at a particularly apt moment in my life.  External forces have encouraged me to reflect on the role that nutrition plays in my life.  In particular, I have become interested in whole-food plant-based nutrition, and so, at the beginning of the module (knowing that it would deal with data), I contemplated creating a site that would use data related to the subject in some fashion.  Coincidentally, on completing the module, I discovered that it was an online cookbook was a suggested project idea.

The primary purpose of the project is to provide a site that will encourage users to **_JOIN THE REVOLUTION_** and **_EXPLORE AND SHARE_** healthy whole-food plant-based recipes.  Naturally, the second goal of the project is to demonstrate my ability to create a site that is driven by data.

The site contains a large call-to-action, contains imagery and colors that suggest health and vitality, and prevents users from commenting or submitting recipes unless they create an account; unless they **_JOIN_** the revolution.  Further encouragement is offered by allowing users' recipes to become **_Most Popular Recipe_** and **_Recipe of the Week_**, thereby creating a sense of competition.

The incorporation of HTML, CSS, JavaScript and Python elements in an organised, well-structured manner should satisfy the last goal of displaying the developers's talents as a junior web developer.


***
## UX 

### Initial design decisions

As a subscriber to the [Forks Over Knives](https://www.forksoverknives.com) newsletter, I began by reviewing the mailings that land in my inbox regularly, seeking inspiration.  Further design inspiration was gathered by visiting the following sites:

* [Food52](https://food52.com/recipes/)
* [allrecipes](https://www.allrecipes.com/)
* [Jamie Oliver](https://www.jamieoliver.com)
* [CookEatShare](https://cookeatshare.com/)


### Strategy & Planning
The UX design process revolves around a mobile-first design.  As the site revolves around the subject of healthy eating the predominantly green colour scheme provides a sense of relaxation, growth and success.  Large images of the recipes are used to entice users to **_Explore_** the site **_& Share_** their own recipe ideas.

The design could also be seen to reflect trends in the field as both the Jamie Oliver and Forks over Knives websites use similar imagery and colour scheme.


#### User Stories
* As a casual user I want an engaging site that provides simple, clear recipes that I can use to enhance my diet.
* As an engaged user I want a platform where I can view, use and comment on others' recipes, and share and receive feedback on my own recipes.
* As a novice developer, I am looking for a platform to showcase my web development abilities. 


### Scope
The scope of the project was restricted to the creation of a base site the provided the ability to create, read, update and delete recipes.  The basic framework also provides for expansion, at a later date.  The provision of **Recipe of the Week** and **Most Popular Recipe** are indicative of the a user ranking system.  The various elements that were included in the core scope include:

* A landing page that clearly indicates the broad nature of the site.  This is quickly followed by the call-to-action, which informs the user, in a precise and concise manner as to the deeper nature of the site.
* The ability for users to quickly search the site for recipes
* The ability for users to quickly **Join the Revolution** (sign up or login)
* The ability for users to quickly submit recipes, with a clear message that they need to login to do so
* Clear navigation that responds to the user login status


### Structure
The site incorporate a main navigation menu and structured layout (using Bootstrap to accomplish this).

Casual users can read recipes on the site freely but are encouraged to become engaged users.  Engaged users are rewarded with additional functionality.  They can store and manipulate data in the form of their own user details and the recipes they submit.  Furthermore, they may comment on their own and other users' recipes.

A great deal of effort has gone into the design of the database schema.  It is hoped that it is both well-suited to the domain and makes intelligent use of MongoDB's features.


### Skeleton

As one might expect the project was developed on two fronts, the front-end (or view) and the backend (or database). In order to provide an overview, and aid in guiding preliminary design decisions, an [ideas board](https://res.cloudinary.com/bogtrotter72/image/upload/v1589877905/wfpblife/Preliminary_Design_Ideas/Ideas_Board_qxxp5g_uwnnaq.pdf) was created with cuttings from the sites mentioned in **Initial Design Decision** above, using [Mind Architect](https://www.ambiera.com/mindarchitect/).  These ideas informed the development, in part, of both the wireframe and database.  To demonstrate the intricate design - database relationship, the _Forks over Knives_ newsletter had, what I perceived to be an interesting layout; a large recipe at both the top and bottom with several, smaller recipes inbetween.  While the larger recipes are not presented with any explicit declaration of their importance, in the _Forks over Knives_ newsletter, I felt that, as size often suggests importance, I would modify the design.  By embedding a _ratings_ document into the _recipes_ document in the database, I would be able to query the data for _Recipe of the Week_ and _Most Popular Recipe_.  In addition, I felt that this would serve as an incentive to user to:
* Sign up (so that they could submit recipes)
* Improve on the quality of their recipe submissions (in order to gain _top billing_)
* Increase frequency of visits (checking on recipe performance)

The design of wireframe and database continued in this manner, first one driving the process and then the other. The initial database schema designs were sketched out using [Moon Modeler](https://www.datensen.com/data-modeling/moon-modeler-for-databases.html), data modeling tool for MongoDB, while the wireframe was being designed in [Balsamiq](https://balsamiq.com).  A pdf of the wireframes is available [here](https://res.cloudinary.com/bogtrotter72/image/upload/v1591285825/wfpblife/Preliminary_Design_Ideas/bmhcjynbkpxewpmwfepg.pdf).  


### Surface
The aesthetic of the site is clean, fresh and suggestive of the potential gains in terms of health and vitality, from choosing a whole-food, plant-based diet. The idea for the colours reflect those from the **Jamie Oliver** site and the **Forks Over Knives** newsletter
 is purposefully designed to have a relaxing yet playful feel.  This conscious design decision was made in an attempt to counteract the stress of preparing for tests.  The background is designed to subtly mirror the block graphic used in the game.  Its colours match those in the game and are muted to reinforce the background positioning.

### Design Decisions
The next phase of the design process revolved around creating mock data to populate the fields, as laid out in the schema.  It was felt that this would prove the schema design and highlight any difficulties in querying the database, prior to committing the design to code.

The tools used to achieve this included the command line, [Mongo Shell](https://docs.mongodb.com/manual/mongo/), [Robo 3T](https://robomongo.org/), [Moon Modeler](https://www.datensen.com/data-modeling/moon-modeler-for-databases.html) and [Mockaroo](https://www.mockaroo.com). While Mockaroo proved useful in creating some of the test data, a solution has yet to be found to the problem of creating data in the required formats for MongoDB.

Developer tools were used extensively to ensure a good balance between font sizes and to assist in positioning items on the screen.

***
## Features
### Existing features
* **Responsive Navigation** - The navigation items adapt to the user's login status - displaying _signup_ and _login_ if the user is not logged in and _account_ and _logout_ if they are.
* **Dynamic Form Fields** - The recipe submission form provides users with the ability to dynamically add and remove ingredient and method elements. The icons are clear indicators of this functionality.
* **Data handling** - Users can store and manipulate recipe data records and personal information.
* **User functionality** - Users are encouraged to explore and share their recipes, and are provided with the entire range of CRUD functionality.


### Planned features 
* Improved user dashboard to include:
    * ranking for **Most frequent visitor**, **Most active contributor** and **Most active reviewer**
    * recipe performance (number of views, ratings, etc.)
    * recipe download or print facility
* To maintain content quality the site could incorporate moderation (initially from the site owner but then through volunteer moderators)
* To improve user experience by including _Forgotten Password_ functionality

***
## Technologies Used
* [HTML](https://en.wikipedia.org/wiki/HTML) - Providing the basic structure for content.
* [CSS](https://en.wikipedia.org/wiki/Cascading_Style_Sheets) - Styling the site, providing responsive design and adding button animations.
* [JavaScript](https://en.wikipedia.org/wiki/JavaScript) - Adding a small amount of functionality to the site. 
* [JQuery](https://jquery.com/) - Supporting library for much of the JavaScript functionality. 
* [Balsamiq](https://balsamiq.com/) - Creating wireframes at project inception

***
## Testing 

Preliminary tests of the database used fake (test) data created in Mockaroo and adjusted slightly to required format required by MongoDB. Both [MongoDB Compass](https://www.mongodb.com/products/compass) and [Studio3T](https://studio3t.com/) proved useful in experimenting with the aggregation framework.

All CRUD operation were checked, including:
* Creating a user account, recipes and comments
* Searching for recipes, and filtering these by popularity and author
* Entering search parameters directly into the url for recipes not in the database (and providing a suitable 404 response)
* Viewing recipes
* Updating user account details, recipes and comments (including attempting to update recipes where user is not recipe owner)
* Deleting user account details, recipes and comments


### Manual Testing
Throughtout the project, the terminal window was used extensively, in combination with print statements in the code, to check feedback from the database and from user input.

All clickable elements were thoroughly tested, in order to identify any bugs that might occur through multiple function calls, double-click events, etc.

The appearance and performance of the game was checked by the developer on multiple devices, including desktop, laptop and mobile screens.  Friends and family also tested the game on mobile and desktop environments and provided verbal feedback.  The results of the initial feedback are most apparent in the deviation from the original wireframe design.  Users requested almost immediate game access and limited button clicks.

The website was also tested in the Blisk browser, on a variety of devices, including:
* Samsung Galaxy S5
* iPhone 5/SE
* iPhone 6/7/8
* iPhone X
* iPad
* iPad Pro

Chrome and Blisk developer tools were used for testing the site, and were of particular use in positioning the graphics and confirming control flow.

### Cross-Browser Compatability
The website was tested in the following browsers:
* Blisk
* Firefox
* Google Chrome
* Microsoft Edge
* Opera

### Live Testing
The project was viewed and tested on mobile tablet, laptop and desktop devices.  Work colleagues, friends and families were invited to review and feedback on the site; all of which positive.  The site was thoroughly tested by my mentor and I am grateful to him for expanding my understanding of testing.  Live testing, therefore, also included entering nonsensical data (strings and integers) directly into the url. Failure during some tests led to the addition of a 404 error handler and additional catch elements in the code. It is hoped that these will suffice in _handling errors gracefully_.


### Interesting bug - resolved
Initially sign up and login elements were designed as modals but during testing some difficulty was encountered while they were on the same page. It began with an inability to switch between modals, which was resolved through a simple code fix. Next, on testing form validation and error messages on the sign up modal, validation and error messages would display as expected until all 4 fields were populated, with a matching error between the _password_ and _confirm password_ fields. In this instance the form would appear to submit, with the error only displaying once the modal was reopened. This bug was resolved by simply replacing the modals with separate pages.

### Interesting bug - remaining




Also followed along with [Corey Schafer’s](https://www.youtube.com/user/schafer5/) Flask YouTube tutorial series.

The auto-resizing textarea code was provided by [James Padolsey](https://j11y.io/demos/plugins/jQuery/autoresize.jquery.js) and has not been altered. Thanks to [CSS tricks](https://css-tricks.com/textarea-tricks/) for the tip.