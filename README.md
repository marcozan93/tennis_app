# tennis_app
## Comparing ATP players performance over 10 years

This is an example of a short Exploratory Data Analysis project to compare the performance of specific tennis players over 10 years (2009-2019).

The project has been developed in python3 using *pandas, numpy, sklearn* for data manipulation, and *plotly and dash* for data visualisation.
The app is currently hosted on *heroku* at https://tennis-atp-app-mz.herokuapp.com/

Data collection: data were collected from this https://github.com/JeffSackmann/tennis_atp public repository.

The average statistics for each player are diplayed and the user can compare two players based on their average performance.
An example is provided below for Federer vs Nadal.

### Data labels
- **ace**: number of aces
- **df**: number of doubles faults
- **svpt**: number of serve points
- **1stIn**: number of first serves made
- **1stWon**: number of first-serve points won
- **2ndWon**: number of second-serve points won
- **SvGms**: number of serve games
- **bpSaved**: number of break points saved
- **bpFaced**: number of break points faced
- **ioc**: international olympic commettee

![Screenshot 2022-04-13 19 30 42](https://user-images.githubusercontent.com/67830462/163248605-0c486ade-3b1d-4dff-bd21-f0ac8ace4f09.png)
