# WFPB LIFE

### Data Driven Milestone Project

This project comes at a particularly apt moment in my life.  External forces have encouraged me to reflect on the role that nutrition plays in my life.  In particular, I have become interested in whole-food plant-based nutrition, and so, at the beginning of the module (knowing that it would deal with data), I contemplated creating a site that would use data related to the subject in some fashion.  Coincidentally, on completing the module, I discovered that it was an online cookbook was a suggested project idea.

The project itself, however, has been designed to fulfil several key goals.

***

### Research Phase

#### Initial design decisions

As a subscriber to the [Forks Over Knives](https://www.forksoverknives.com) newsletter, I began by reviewing the mailings that land in my inbox regularly, seeking inspiration.  Further design inspiration was gathered by visiting the following sites:

* [Food52](https://food52.com/recipes/)
* [allrecipes](https://www.allrecipes.com/)
* [Jamie Oliver](https://www.jamieoliver.com)
* [CookEatShare](https://cookeatshare.com/)

In order to provide an overview and aid in guiding preliminary design decisions, an [ideas board](https://res.cloudinary.com/bogtrotter72/image/upload/v1588316744/Milestone%203/Preliminary_Design_Ideas/Ideas_Board_qxxp5g.pdf) was created with cuttings from these sites, using [Mind Architect](https://www.ambiera.com/mindarchitect/).  These ideas were then incorporated, in parallel, into the designs of the wire frame and database.  By way of example, the initial database schema designs were sketched out using [Hackolade](https://hackolade.com), while the wire frame was being designed in [Balsamiq](https://balsamiq.com).  The _user_ collection mirrors the _sign up_ modal, both containing fields for username, email address and password.  Later in the design of the _user dashboard_ wire frame, it became apparent that the _user_ collection would need to be expanded to include a _login count_, _recipe count_ and _comment count_ to facilitate database queries regarding the user’s activity on the site.  The design of wire frame and database continued in this manner, first one driving the process and then the other.

#### Continuing design

The next phase of the design process revolved around creating mock data to populate the fields, as laid out in the schema.  This would prove its design and highlight any difficulties in querying the database, prior to committing the design to code.

Tools used to achieve this included the command line, [Mongo Shell](https://docs.mongodb.com/manual/mongo/), [Robo 3T](https://robomongo.org/), Hackolade and [Mockaroo](https://www.mockaroo.com). While Mockaroo proved useful in creating some of the test data, a solution has yet to be found to the problem of creating data in the required formats for MongoDB.  The orders collection, for example, was created as a JSON array, where an embedded document was required.  Furthermore, each value in the address array was randomised, creating non-existent values that were of no use for geospatial queries.  [Generate Plus](https://generate.plus/en/address) was, therefore, used to replace the values with real addresses.






### Interesting bug - resolved
During testing of the sign up and login modals, some difficulty was encountered while they were on the same page. It began with an inability to switch between modals, which was resolved through a simple code fix. Next, on testing form validation and error messages on the sign up modal, validation and error messages would display as expected until all 4 fields were populate, with a matching error between the _password_ and _confirm password_ fields. In this instance the form would appear to submit, with the error only displaying once the modal was reopened. This bug was resolved by simply placing the modal on separate pages and using links.

### Interesting bug - remaining
Having modals on .








Also followed along with [Corey Schafer’s](https://www.youtube.com/user/schafer5/) Flask YouTube tutorial series.

The auto-resizing textarea code was provided by [James Padolsey](https://j11y.io/demos/plugins/jQuery/autoresize.jquery.js) and has not been altered. Thanks to [CSS tricks](https://css-tricks.com/textarea-tricks/) for the tip.