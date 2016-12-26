
# coding: utf-8
# The original blog post for this notebook is at: https://umar-yusuf.blogspot.com.ng/2016/12/nairaland-christmas-birthday-analyzed.html
# In[1]:

# import the libraries we are going to use

# libraries for Scraping and Cleaning the data
import re
import requests
from bs4 import BeautifulSoup


# libraries for Analyzing and Visualizing the data
import pandas as pd
from datetime import datetime


# In[2]:

# Scraping out the raw html code of nairaland home page
url = "http://www.nairaland.com/home"
raw_html = requests.get(url) # returns the complete url html code

# print (raw_html.text)

raw_data = raw_html.text  # save the text in an object

soup_data = BeautifulSoup(raw_data, "lxml") # use BeautifulSoup module read the html into xml to and save it in an object


# In[3]:

# lets display only the part of the data we need. It is contained in the cell of table tag (<td>)

soup_data("td")


# In[4]:

# lets read out the text only ignoring the tag cell in a table
for data in soup_data("td"):
    print (data.text)


# In[5]:

# Obviously, we don't need every text above. So use the 're' module, to extract only the relevant birthday list

# Note: I will ignore those members whose ages are not displayed, so that we don't have to deal with NaN values in our data


member_found = None

re_match = "[\w]+\([\d]+\)" # any word count+1 followed-by '(' followed-by any number count+1 followed-by ')'

for data in soup_data("td"):
    data_found = re.findall(re_match, data.text)
    
    if data_found:
        member_found = data_found

print (member_found)


# In[6]:

# Lets further clean up the list to seperate Usernames from age

# Use list comprehension to replace the last brace ")" with empty "" in member_found above


member_found_replaced = [x.replace(")", "") for x in member_found]            # replaces ")" by ""

print (member_found_replaced)


# In[7]:

# Now split "member_found_replaced" based on '(' between the usernames and age
# we use for loop to loop through each item of the "member_found_replaced" list above

for y in member_found_replaced:
    member_cleaned = y.split("(")
    print (member_cleaned)
    
# what we have "member_cleaned" is individual list with two elements each
# lets combine all the lists into a dictionary


# In[8]:

# we first declare "member_cleaned" as empty dictiory, so we can append individaul list above into it

member_cleaned = {}

for y in member_found_replaced:
    temp_data = y.split("(")
    
    member_cleaned[temp_data[0]] = int(temp_data[1])
    
print (member_cleaned)


# In[9]:

# covert the dictionary "member_cleaned" above into a Pandas DataFrame
# Note: in python 3, we have to convert the dictionary items into a list to work with Pandas DataFrame


# define the column names
columns_name = ["Username", "Age"]

# df = pd.DataFrame(member_cleaned.items(), columns = columns_name )   # this is for python 2
df = pd.DataFrame(list(member_cleaned.items()), columns = columns_name )

df


# In[10]:

# Lets add a column for today's date

# using the datetime module


todays_date = datetime.now().date()

df["Date"] = todays_date

df


# In[11]:

# Let save the dataframe into csv file
# we name the csv file with the current date, i.e: 14/08/2016 will be 20160814 for the file name

csv_name = todays_date.strftime("%Y%m%d")

df.to_csv(csv_name + ".csv")


# # Now our christmas birthday dataset is saved in a CSV file future use...

# In[ ]:



