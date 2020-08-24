# LibP2P Address Convertr - Heroku App



## heroku deployment notes

```console
### one time
$ heroku create  # create app
$ heroku ps:scale web=1

### for every modification
$ git push heroku master  # deploy app

### after deployment
$ heroku open  # open heroku webapp
$ heroku logs — tail  # tail remote logs
``` 
