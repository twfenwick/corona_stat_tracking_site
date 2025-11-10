# Corona Stat Tracking Site #

### Purpose ###

This is a simple web application to track COVID-19 statistics around the US by state and/or county. I created it as a
pastime during the pandemic in an effort to be more informed about infection rates and trends near me. And also to kill
time. The problem then was that most COVID-19 tracking sites were too general being at the national or state 
level and I wanted to know what was going on in my area, like how risky was it to go to the grocery store, and be able
to reference something quickly to visually reflect the latest trends. This site allowed users to track COVID-19 
statistics at the county level, which was more useful in determining the status and safety of the surrounding area. 

In time, during the pandemic there were indeed improved and more polished sites for conveniently presenting this data 
visually, but it still has some use for educational purposes as a tool for learning and applying new skills and 
technologies.

The data was sourced from the New York Times COVID-19 data repository on GitHub: 
https://github.com/nytimes/covid-19-data.git which is no longer updated as of March 2023. Please note, the initial pull
from the nytimes repository to local takes a few minutes as it is a large dataset. It is fetched only once at server start and
pulled into the project root, so you may want to pull it separately to avoid the wait during runtime.

### Run Locally ###
From the project root directory, run:
`python manage.py runserver`

Then open a web browser (to show US stats):
http://127.0.0.1:8000/dailystats/ or
http://127.0.0.1:8000/dailystats/us/

To view by state, use the two-letter state code, e.g. for California:
http://127.0.0.1:8000/dailystats/CA/

To view by county, use the two-letter state code and the county name, e.g. for Orange County, CA:
http://127.0.0.1:8000/dailystats/CA/orange

Use the legend to the right to turn on and off statistics and the tools at the top for further interaction.

### Deploy to AWS Elastic Beanstalk ###
For a quick and simple deployment to AWS Elastic Beanstalk, you can use the django instructions starting from deployment
here: https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-django.html#python-django-deploy
(configuration files should be good to go already in the .ebextensions and .elasticbeanstalk directories). Note you'll
need to get the CNAME from `eb status` after creating the application environment and add it to the allowed hosts in 
settings.py before deploying. You might need to commit the change locally before deploying with `eb deploy`. This will
be your host unless mapped to a specified domain.

You will also need to increase the size of the disk on the EC2 instance (32GB should work) as the default 8GB is not enough to
pull in the nytimes data repository. Subsequently, the time to pull the data is painstakingly long on the small instance
type compared to your local machine capabilities. Hopefully, this will be improved by migrating the data to
a Dynamo or other DB and removing this need altogether, since the dataset is now static.

