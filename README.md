# Piggy/SPLIT
#### Video Demo:  <URL HERE>
#### Description:
Splitting costs with friends just got easier!

This app is your new best friend when it comes to handling shared expenses with your group, whether it's a local dinner or an international adventure.

Here's how it works:

+ Create a trip or event: Add a description and invite your friends.
+ Track spending: Record shared and individual costs, including who paid for what.
+ Settle up in a snap: The app calculates who owes whom and suggests how much.

No more awkward calculations or keeping track of who owes what. This app takes the hassle out of splitting costs, keeping your friendships (and finances) happy!

## How it works

### Registration and Log-in

First an account needs to be created to use this app. if user is not logged in, the app will redirect the user to the login screen from every other page except the home page. 

If user does not have an account, user first needs to register an account by going to the register link in the navigation bar.

This link will take the user to the register route where user can create a new user id and password. The create button is not enabled unless the password matches in two different fields. The account creation is implemented through the werkzeug library. Only the password hash is stored in the database in the server.

Once registration is complete, user can use the log-in route to log in into the app with the user name and password. Doing this will display the user name of the currently logged in user in the nav bar.

### Creating Trips:

In order to create trips / events, user needs to go to the trips route from the nav bar. 

In this screen, user will have to input trip name and optionally can record a small description so that it is easier to relate for all users involved and click create button to create the trip

The trip will be created in "open" status and it will immidiately be displayed in the screen. the trip can be selected from this space to move to input the participants of this trip.

Alternatively the participants of each trip can be inputted by going to the participants route. 

### Adding Participants

If user comes to this route by clicking the link in the nav bar, first user will need to select the trip from a list of open trips. 

In this screen the trip creator needs to specify which users are the participants of the trip. 

User will be shown a list of potential users that can be added as a participant

Currently 




