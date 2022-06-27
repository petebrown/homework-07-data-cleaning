#!/usr/bin/env python
# coding: utf-8

# # Homework 7, Part Two: A dataset about dogs.
# 
# Data from [a FOIL request to New York City](https://www.muckrock.com/foi/new-york-city-17/pet-licensing-data-for-new-york-city-23826/)

# ## Do your importing and your setup

# In[1]:


import pandas as pd


# ## Read in the file `NYC_Dog_Licenses_Current_as_of_4-28-2016.xlsx` and look at the first five rows

# In[2]:


df = pd.read_excel('NYC_Dog_Licenses_Current_as_of_4-28-2016.xlsx', nrows=30000, na_values=['Unknown', 'UNKNOWN'])
df.head(5)


# ## How many rows do you have in the data? What are the column types?
# 
# If there are more than 30,000 rows in your dataset, go back and only read in the first 30,000.
# 
# * *Tip: there's an option with `.read_csv` to only read in a certain number of rows*

# In[3]:


df.shape


# In[4]:


df.info()


# ## Describe the dataset in words. What is each row? List two column titles along with what each of those columns means.
# 
# For example: “Each row is an animal in the zoo. `is_reptile` is whether the animal is a reptile or not”

# This dataset contains information about licenses issued for dogs in NYC.
# 
# `Owner Zip Code`: Zip code where the owner lives
# 
# `Animal Name`: The name of the animal
# 
# `Animal Gender`: The gender of the animal
# 
# `Primary Breed`: The primary breed of the animal
# 
# `Secondary Breed`: The secondary breed of the animal (where applicable)
# 
# `Animal Dominant Color`: The animal's main colour
# 
# `Animal Secondary Color`: The animal's secondary colour (where applicable)
# 
# `Animal Third Color`: The animal's third colour (where applicable)
# 
# `Animal Birth`: The animal's date of birth
# 
# `Spayed or Neut`: Yes/No depending on where the animal is spayed/neutered
# 
# `Guard or Trained`: Yes/No depending on whether the animal is a guard dog or has received training
# 
# `Vaccinated`: Yes/No depending on vaccination status
# 
# `Application Date`: Date and time of application
# 
# `License Issued Date`: Date license was issued
# 
# `License Expired Date`: Date license expires

# # Your thoughts
# 
# Think of four questions you could ask this dataset. **Don't ask them**, just write them down in the cell below. Feel free to use either Markdown or Python comments.

# 1. What proportion of dogs are not vaccinated?
# 2. Which zip code has the most unspayed/unneutered dogs?
# 3. What is the most popular name for Rottweilers?
# 4. On average, are males or females more likely to be unspayed/unneutered?

# # Looking at some dogs

# ## What are the most popular (primary) breeds of dogs? Graph the top 10.

# In[5]:


df['Primary Breed'].value_counts().head(10).plot.bar()


# ## "Unknown" is a terrible breed! Graph the top 10 breeds that are NOT Unknown
# 
# * *Tip: Maybe you want to go back to your `.read_csv` and use `na_values=`? Maybe not? Up to you!*

# In[6]:


# added na_values = 'Unknown' to the initial pd.read_excel()


# ## What are the most popular dog names?

# In[7]:


df['Animal Name'].value_counts().head(10)


# ## Do any dogs have your name? How many dogs are named "Max," and how many are named "Maxwell"?

# In[8]:


df[df['Animal Name'] == 'Pete']['Animal Name'].value_counts()


# In[9]:


df[(df['Animal Name'] == 'Max') | (df['Animal Name'] == 'Maxwell')]['Animal Name'].value_counts()


# ## What percentage of dogs are guard dogs?

# In[10]:


df['Guard or Trained'].value_counts(normalize=True) * 100


# ## What are the actual numbers?

# In[11]:


df['Guard or Trained'].value_counts()


# ## Wait... if you add that up, is it the same as your number of rows? Where are the other dogs???? How can we find them??????
# 
# Use your `.head()` to think about it, then you'll do some magic with `.value_counts()`. Think about missing data!

# In[12]:


df['Guard or Trained'].head()


# ## Maybe fill in all of those empty "Guard or Trained" columns with "No"? Or as `NaN`? 
# 
# Can we make an assumption either way? Then check your result with another `.value_counts()`

# In[13]:


df['Guard or Trained'].value_counts(dropna=False)


# ## What are the top dog breeds for guard dogs? 

# In[14]:


df[df['Guard or Trained'] == 'Yes']['Primary Breed'].value_counts()


# ## Create a new column called "year" that is the dog's year of birth
# 
# The `Animal Birth` column is a datetime, so you can get the year out of it with the code `df['Animal Birth'].apply(lambda birth: birth.year)`.

# In[15]:


df['year'] = df['Animal Birth'].apply(lambda birth: birth.year)
df.head()


# ## Calculate a new column called “age” that shows approximately how old the dog is. How old are dogs on average?

# In[16]:


df['age'] = 2022 - df.year
df.age.mean()


# # Joining data together

# ## Which neighborhood does each dog live in?
# 
# You also have a (terrible) list of NYC neighborhoods in `zipcodes-neighborhoods.csv`. Join these two datasets together, so we know what neighborhood each dog lives in. **Be sure to not read it in as `df`, or else you'll overwrite your dogs dataframe.**

# In[17]:


neighborhoods_df = pd.read_csv('zipcodes-neighborhoods.csv')
df = df.merge(neighborhoods_df, left_on='Owner Zip Code', right_on='zip')
df.head(5)


# ## What is the most popular dog name in all parts of the Bronx? How about Brooklyn? The Upper East Side?
# 
# You'll want to do these separately, and filter for each.

# In[18]:


df[df.borough == 'Bronx']['Animal Name'].value_counts().nlargest(1)


# In[19]:


df[df.borough == 'Brooklyn']['Animal Name'].value_counts().nlargest(1)


# In[20]:


df[df.neighborhood == 'Upper East Side']['Animal Name'].value_counts().nlargest(1)


# ## What is the most common dog breed in each of the neighborhoods of NYC?
# 
# * *Tip: There are a few ways to do this, and some are awful (see the "top 5 breeds in each borough" question below).*

# In[21]:


df.groupby('neighborhood')['Primary Breed'].value_counts().groupby(level=0).head(1)


# In[22]:


# This is the answer I initially cobbled together using StackOverflow. The values are missing, but it looks nicer!
df.groupby('neighborhood')['Primary Breed'].agg(pd.Series.mode).to_frame()


# ## What breed of dogs are the least likely to be spayed? Male or female?
# 
# * *Tip: This has a handful of interpretations, and some are easier than others. Feel free to skip it if you can't figure it out to your satisfaction.*

# This is the solution I was help towards in office hours, but I don't think it answers the question very effectively! e.g. Here I can only see one example of a breed where 100% have _not_ been spayed/neutered, which is what I understood to question to be asking.

# In[23]:


df.groupby('Primary Breed')['Spayed or Neut'].value_counts(normalize=True).sort_values(ascending=False)


# In[24]:


df.groupby('Animal Gender')['Spayed or Neut'].value_counts(normalize=True).sort_values(ascending=False)



# Below is the longwinded solution I originally came up with before consulting a TA.
# 
# It is far less elegant than the single line of code above, but it filters down to just breeds where 100% were unspayed, which was my interpretation of the question.

# In[25]:


spayed_df = df.groupby(['Primary Breed', 'Spayed or Neut'])\
    .agg(total = ('Spayed or Neut', 'count'))\
    .reset_index()

spayed_pivot = spayed_df.pivot(index = 'Primary Breed', columns = 'Spayed or Neut', values = 'total').fillna(0)

spayed_pivot['total'] = spayed_pivot.No + spayed_pivot.Yes
spayed_pivot['pc_unspayed'] = (spayed_pivot.No / spayed_pivot.total) * 100

spayed_pivot.query("pc_unspayed == pc_unspayed.max()").sort_values(by=['pc_unspayed', 'total'], ascending = False)


# In[26]:


spayed_df = df.groupby(['Animal Gender', 'Spayed or Neut'])\
    .agg(total = ('Spayed or Neut', 'count'))\
    .reset_index()

spayed_pivot = spayed_df.pivot(index = 'Animal Gender', columns = 'Spayed or Neut', values = 'total', )
spayed_pivot = spayed_pivot.fillna(0)

spayed_pivot['total'] = spayed_pivot.No + spayed_pivot.Yes
spayed_pivot['pc_unspayed'] = (spayed_pivot.No / spayed_pivot.total) * 100

spayed_pivot.sort_values(by = 'pc_unspayed', ascending = False)


# ## Make a new column called `monochrome` that is True for any animal that only has black, white or grey as one of its colors. How many animals are monochrome?

# In[27]:


df['Animal Dominant Color'] = df['Animal Dominant Color'].str.upper()
df['Animal Secondary Color'] = df['Animal Secondary Color'].str.upper()
df['Animal Third Color'] = df['Animal Third Color'].str.upper()

mono_colors = ['BLACK', 'WHITE', 'GREY']


# I discussed this with Ilena at office hours.
# 
# My interpretation of the question was that we were being asked to assign `True` if an animal (a) only had one color in `Animal Dominant Color`, `Animal Secondary Color Animal` or `Third Color` and (b) that color was black, white or grey.
# 
# I'm sure my solution is overly complicated. I am looking forward to seeing a simpler solution!

# In[28]:


def check_colors(*colors):
    n_colors = 0
    n_mono = 0
    for color in colors:
        if type(color) == str:
            n_colors += 1
            if color in mono_colors:
                n_mono += 1
    if n_colors == 1 and n_mono == 1:
        return True
    else:
        return False

df['monochrome'] = df.apply(lambda x: check_colors(x['Animal Dominant Color'], x['Animal Secondary Color'], x['Animal Third Color']), axis = 1)
df.monochrome.sum()


# ## How many dogs are in each borough? Plot it in a graph.

# In[29]:


df.borough.value_counts().plot(kind='bar')


# ## Which borough has the highest number of dogs per-capita?
# 
# You’ll need to merge in `population_boro.csv`

# In[30]:


boro_pops = pd.read_csv('boro_population.csv')

# Calculate value counts for total dogs in each borough
dogs_per_borough = df.borough.value_counts().reset_index()
# Rename columns
dogs_per_borough = dogs_per_borough.rename(columns = {'index': 'borough', 'borough': 'n_dogs'})
# Merge with data population csv
dogs_per_borough = dogs_per_borough.merge(boro_pops, left_on = 'borough', right_on = 'borough')
# Calculate dogs per capita in each borough
dogs_per_borough['dogs_per_capita'] = dogs_per_borough.n_dogs / dogs_per_borough.population

# Sort dataframe so borough with highest dogs per capita is top
dogs_per_borough.sort_values('dogs_per_capita', ascending=False)


# ## Make a bar graph of the top 5 breeds in each borough.
# 
# How do you groupby and then only take the top X number? You **really** should ask me, because it's kind of crazy.

# Below is the solution I arrived at after attending office hours.

# In[31]:


df.groupby('borough')['Primary Breed'].value_counts().groupby(level=0).head(5).plot.barh()


# Below is the solution I originally came up with before going to office hours. I interpreted the question to mean we needed separate graphs showing the top 5 breeds for each borough!

# In[32]:


boroughs = df.borough.unique()
top_5_df = pd.DataFrame()

for borough in boroughs:
    temp_df = df[df.borough == borough]['Primary Breed'].value_counts().nlargest(5).to_frame().reset_index()
    temp_df['borough'] = borough
    top_5_df = pd.concat([top_5_df, temp_df])

top_5_df = top_5_df.rename(columns = {'index': 'primary_breed',
                                      'Primary Breed': 'count'})

for borough in boroughs:
    top_5_df[top_5_df.borough == borough].plot.bar(x = 'primary_breed', y = 'count', title = borough, xlabel="", legend=False)


# In[ ]:




