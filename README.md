# sqlalchemy-challenge

<h1>Part 1: Climate Analysis and Exploration</h1>
<p>Started by importing all the necessary dependencies and then reflected the tables from the DB and set them up as 'Measurement' and 'Station'</p>
<p>I used a straightforward query to get the last date from the measurement table then used timedelta to get the one year ago date. Once I had my dates I initially set up a straightforward query to select date and prcp between the dates identified, then also set up a query to get the data using the Measurement class. I loaded my query results into a dataframe and then sorted by date so that I could graph the results.</p>
<p>I used .agg on the dataframe to calculate the summary stats on precip. Then used a straightforward query to find the station IDs.</p>
<p>For the count of stations I did a standard query first, then wrote it using the classes to get it another way. Both times grouped by station and ordered by count descending.</p>

