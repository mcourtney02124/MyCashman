This is my version of the "cashman" application described at
https://auth0.com/blog/developing-restful-apis-with-python-and-flask/#bootstrapping-flask

I copied that flask application and added to it (a couple more
REST interfaces, plus a sketchy IVR implemented with SIPp scripts)
so I could experiment with testing a REST API with pytest, and Tavern, 
and run all that with Jenkins.

Not using Docker for now, that will need serious rework when I come
back to it. Environmental dependencies include SIPp, pytest, Tavern ...
