# WFPB LIFE

### Data Driven Milestone Project

This project comes at a particularly apt moment in my life.  External forces have encouraged me to reflect on the role that nutrition plays in my life.  In particular, I have become interested in whole-food plant-based nutrition, and so, at the beginning of the module (knowing that it would deal with data), I contemplated creating a site that would use data related to the subject in some fashion.  Coincidentally, on completing the module, I discovered that it was an online cookbook was a suggested project idea.

The primary purpose of the project is to provide a site that will encourage users to _JOIN THE REVOLUTION_ and _EXPLORE AND SHARE_ healthy whole-food plant-based recipes.  Naturally, the second goal of the project is to demonstrate my ability to create a site that is driven by data.

The site contains a large call-to-action, contains imagery and colors that suggest health and vitality, and prevents users from commenting or submitting recipes unless they create an account; unless they _JOIN_ the revolution.  Further encouragement is offered by allowing users' recipes to become _Most Popular Recipe_ and _Recipe of the Week_, thereby creating a sense of competition.

The incorporation of HTML, CSS, JavaScript and Python elements in an organised, well-structured manner should satisfy the last goal of displaying the developers's talents as a junior web developer.


***
## UX 

### Initial design decisions

As a subscriber to the [Forks Over Knives](https://www.forksoverknives.com) newsletter, I began by reviewing the mailings that land in my inbox regularly, seeking inspiration.  Further design inspiration was gathered by visiting the following sites:

* [Food52](https://food52.com/recipes/)
* [allrecipes](https://www.allrecipes.com/)
* [Jamie Oliver](https://www.jamieoliver.com)
* [CookEatShare](https://cookeatshare.com/)

In order to provide an overview and aid in guiding preliminary design decisions, an [ideas board](https://res.cloudinary.com/bogtrotter72/image/upload/v1588316744/Milestone%203/Preliminary_Design_Ideas/Ideas_Board_qxxp5g.pdf) was created with cuttings from these sites, using [Mind Architect](https://www.ambiera.com/mindarchitect/).  These ideas were then incorporated, in parallel, into the designs of the wire frame and database.  By way of example, the initial database schema designs were sketched out using [Hackolade](https://hackolade.com), while the wire frame was being designed in [Balsamiq](https://balsamiq.com).  The _user_ collection mirrors the _sign up_ modal, both containing fields for username, email address and password.  Later in the design of the _user dashboard_ wire frame, it became apparent that the _user_ collection would need to be expanded to include a _login count_, _recipe count_ and _comment count_ to facilitate database queries regarding the user’s activity on the site.  The design of wire frame and database continued in this manner, first one driving the process and then the other.


### Strategy & Planning
The UX design process revolves around a mobile-first design.  As the site revolves around the subject of healthy eating the predominantly green colour scheme provides a sense of relaxation, growth and success.  Large images of the recipes are used to entice users to _explore_ the site and _share_ their own recipe ideas.

The design could also be seen to reflect trends in the field as both the Jamie Oliver and Forks over Knives websites use similar imagery and colour scheme.


#### User Stories
* As a casual user I want an engaging site that provides simple, clear recipes that I can use to enhance my diet.
* As an engaged user I want a platform where I can view, use and comment on others' recipes, and share and receive feedback on my own recipes.
* As a novice developer, I am looking for a platform to showcase my web development abilities. 


### Scope
The scope of the project was restricted to the creation of a base site the provided the ability to create, read, update and delete recipes.  The basic framework also provides for expansion, at a later date.  The provision of _Recipe of the Week_ and _Most Popular Recipe_ are indicative of the a user ranking system.  The various elements that were included in the core scope include:

* A landing page that clearly indicates the broad nature of the site.  This is quickly followed by the call-to-action, which informs the user, in a precise and concise manner as to the deeper nature of the site.
* The ability for users to quickly search the site for recipes
* The ability for users to quickly _Join the Revolution_ (sign up or login)
* The ability for users to quickly submit recipes, with a clear message that they need to login to do so
* Clear navigation that responds to the user login status


### Structure
The site incorporate a main navigation menu and structured layout (using Bootstrap to accomplish this).

Casual users can read recipes on the site freely but are encouraged to become engaged users.  Engaged users are rewarded with additional functionality.  They can store and manipulate data in the form of their own user details and the recipes they submit.  Furthermore, they may comment on their own and other users' recipes.

A great deal of effort has gone into the design of the database schema.  It is hoped that it is both well-suited to the domain and makes intelligent use of MongoDB.


### Skeleton

The initial design (below), in practice, served more as an idea's platform or board.  As is apparent in the final design, the first four screens were incorporated into the main page and hidden until required.

A pdf of the wireframes is available [here](https://res.cloudinary.com/bogtrotter72/image/upload/v1582474102/Milestone%202/Final%20Images/Card_Match_Game2_uhqkzf.pdf)

The wireframes were constructed with a mobile platform in mind, however, it was clear that there would be little difficult in scaling the game board for tablet, laptop or desktop devices.

### Surface
As stated, the look of the game is purposefully designed to have a relaxing yet playful feel.  This conscious design decision was made in an attempt to counteract the stress of preparing for tests.  The background is designed to subtly mirror the block graphic used in the game.  Its colours match those in the game and are muted to reinforce the background positioning.

### Design Decisions
The font was chosen to suggest an element of play.  The choice of a simple geometric shape was made following a trial with complex block shapes in three-dimensional space.  Test subjects found the game too difficult and were therefore not encouraged to explore the game further.  More accessible designs were developed in response to this feedback.



#### Continuing design

The next phase of the design process revolved around creating mock data to populate the fields, as laid out in the schema.  This would prove its design and highlight any difficulties in querying the database, prior to committing the design to code.

Tools used to achieve this included the command line, [Mongo Shell](https://docs.mongodb.com/manual/mongo/), [Robo 3T](https://robomongo.org/), Hackolade and [Mockaroo](https://www.mockaroo.com). While Mockaroo proved useful in creating some of the test data, a solution has yet to be found to the problem of creating data in the required formats for MongoDB.  The orders collection, for example, was created as a JSON array, where an embedded document was required.  Furthermore, each value in the address array was randomised, creating non-existent values that were of no use for geospatial queries.  [Generate Plus](https://generate.plus/en/address) was, therefore, used to replace the values with real addresses.






### Interesting bug - resolved
During testing of the sign up and login modals, some difficulty was encountered while they were on the same page. It began with an inability to switch between modals, which was resolved through a simple code fix. Next, on testing form validation and error messages on the sign up modal, validation and error messages would display as expected until all 4 fields were populate, with a matching error between the _password_ and _confirm password_ fields. In this instance the form would appear to submit, with the error only displaying once the modal was reopened. This bug was resolved by simply placing the modal on separate pages and using links.

### Interesting bug - remaining
Having modals on .








Also followed along with [Corey Schafer’s](https://www.youtube.com/user/schafer5/) Flask YouTube tutorial series.

The auto-resizing textarea code was provided by [James Padolsey](https://j11y.io/demos/plugins/jQuery/autoresize.jquery.js) and has not been altered. Thanks to [CSS tricks](https://css-tricks.com/textarea-tricks/) for the tip.