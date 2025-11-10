# Corona Stat Tracking Site #

### Purpose ###

This is a simple web application to track COVID-19 statistics around the US by state and/or county. I created it as a
pastime during the pandemic in an effort to be more informed about infection rates and trends near me. And also to kill
time. The problem then was that most COVID-19 tracking sites were too general being at the national or state 
level and I wanted to know what was going on in my area, like how risky was it to go to the grocery store. 
This site allowed users to track COVID-19 statistics at the county level, which was more useful in determining
the status and safety of the surrounding area. 

In time, during the pandemic there were indeed improved and more polished sites for conveniently presenting this data 
visually, but it still has some use for educational purposes as a tool for learning and applying new skills and 
technologies.

The data was sourced from the New York Times COVID-19 data repository on GitHub: 
https://github.com/nytimes/covid-19-data.git which is no longer updated as of March 2023. Please note, the initial pull
from the nytimes repository takes a few minutes as it is a large dataset. It is fetched only once at server start and
pulled into the project root, so you may want to pull it separately to avoid the wait during runtime.
