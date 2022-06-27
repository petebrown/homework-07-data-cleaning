#!/usr/bin/env python
# coding: utf-8

# # Homework 7, Part One: Lots and lots of questions about beer

# ### Do your importing and your setup

# In[1]:


import pandas as pd


# ## Read in the file `craftcans.csv`, and look at the first first rows

# In[2]:


df = pd.read_csv('craftcans.csv', na_values=['Does not apply'])
df.head(5)


# ## How many rows do you have in the data? What are the column types?

# In[3]:


df.shape


# In[4]:


df.info()


# # Checking out our alcohol

# ## What are the top 10 producers of cans of beer?

# In[5]:


df.Brewery.value_counts().head(10)


# ## What is the most common ABV? (alcohol by volume)

# In[6]:


df.ABV.value_counts().head(1)


# ## Oh, weird, ABV isn't a number. Convert it to a number for me, please.
# 
# It's going to take a few steps!
# 
# ### First, let's just look at the ABV column by itself

# In[7]:


df.ABV


# ### Hm, `%` isn't part of  a number. Let's remove it.
# 
# When you're confident you got it right, save the results back into the `ABV` column.
# 
# - *Tip: In programming the easiest way to remove something is to *replacing it with nothing*.
# - *Tip: "nothing" might seem like `NaN` sinc we talked about it a lot in class, but in this case it isn't! It's just an empty string, like ""*
# - *Tip: `.replace` is usually used for replacing ENTIRE cells, while `.str.replace` is useful for replacing PARTS of cells*

# In[8]:


df.ABV = df.ABV.str.replace("%", "")
df.ABV.head()


# ### Now let's turn `ABV` into a numeric data type
# 
# Save the results back into the `ABV` column (again), and then check `df.dtypes` to make sure it worked.
# 
# - *Tip: We used `.astype(int)` during class, but this has a decimal in it...*

# In[9]:


df.ABV = df.ABV.astype(float)
df.ABV.head()


# ## What's the ABV of the average beer look like?
# 
# ### Show me in two different ways: one command to show the `median`/`mean`/etc, and secondly show me a chart

# In[10]:


df.ABV.describe()


# In[11]:


df.ABV.hist()


# ### We don't have ABV for all of the beers, how many are we missing them from?
# 
# - *Tip: You can use `isna()` or `notna()` to see where a column is missing/not missing data.*
# - *Tip: You just want to count how many `True`s and `False`s there are.*
# - *Tip: It's a weird trick involving something we usually use to count things in a column*

# In[12]:


df.ABV.isna().sum()


# # Looking at location
# 
# Brooklyn used to produce 80% of the country's beer! Let's see if it's still true.

# ## What are the top 10 cities in the US for canned craft beer?

# In[13]:


df.Location.value_counts()


# ## List all of the beer from Brooklyn, NY

# In[14]:


df[df.Location == 'Brooklyn, NY']


# ## What brewery in Brooklyn puts out the most types of canned beer?

# In[15]:


df[df.Location == 'Brooklyn, NY'].Brewery.value_counts().head(1)


# ## What are the five styles of beer that Sixpoint produces the most cans of?

# In[16]:


df[df.Brewery == 'Sixpoint Craft Ales'].Style.value_counts()


# ## List all of the breweries in New York state.
# 
# - *Tip: We want to match **part** of the `Location` column, but not all of it.*
# - *Tip: Watch out for `NaN` values! You might be close, but you'll need to pass an extra parameter to make it work without an error.*

# In[17]:


df[df.Location.str.contains("NY", na=False)].Brewery.unique()


# ### Now *count* all of the breweries in New York state

# In[18]:


df[df.Location.str.contains("NY", na=False)].Brewery.nunique()


# # Measuring International Bitterness Units
# 
# ## Display all of the IPAs
# 
# Include American IPAs, Imperial IPAs, and anything else with "IPA in it."
# 
# IPA stands for [India Pale Ale](https://www.bonappetit.com/story/ipa-beer-styles), and is probably the most popular kind of beer in the US for people who are drinking [craft beer](https://www.craftbeer.com/beer/what-is-craft-beer).

# In[19]:


df[df.Style.str.contains('IPA', na=False)]


# IPAs are usually pretty hoppy and bitter (although I guess hazy IPAs and session IPAs are changing that since I first made this homework!). IBU stands for [International Bitterness Unit](http://www.thebrewenthusiast.com/ibus/), and while a lot of places like to brag about having the most bitter beer (it's an American thing!), IBUs don't necessary *mean anything*.
# 
# Let's look at how different beers have different IBU measurements.

# ## Try to get the average IBU measurement across all beers

# In[20]:


df.IBUs.mean()


# ### Oh no, it doesn't work!
# 
# It looks like some of those values *aren't numbers*. There are two ways to fix this:
# 
# 1. Do the `.replace` and `np.nan` thing we did in class. Then convert the column to a number. This is boring.
# 2. When you're reading in your csv, there [is an option called `na_values`](http://pandas.pydata.org/pandas-docs/version/0.23/generated/pandas.read_csv.html). You can give it a list of **numbers or strings to count as `NaN`**. It's a lot easier than doing the `np.nan` thing, although you'll need to go add it up top and run all of your cells again.
# 
# - *Tip: Make sure you're giving `na_values` a LIST, not just a string*
# 
# ### Now try to get the average IBUs again

# In[21]:


df.IBUs.mean() # Fixed by adding na_values=['Does not apply'] to initial pd.read_csv()


# ## Draw the distribution of IBU measurements, but with *twenty* bins instead of the default of 10
# 
# - *Tip: Every time I ask for a distribution, I'm looking for a histogram*
# - *Tip: Use the `?` to get all of the options for building a histogram*

# In[22]:


df.IBUs.hist(bins=20)


# ## Hm, Interesting distribution. List all of the beers with IBUs above the 75th percentile
# 
# - *Tip: There's a single that gives you the 25/50/75th percentile*
# - *Tip: You can just manually type the number when you list those beers*

# In[23]:


df.IBUs.describe()


# In[24]:


df[df.IBUs > 64].Beer


# ## List all of the beers with IBUs below the 25th percentile

# In[25]:


df[df.IBUs < 21].Beer


# ## List the median IBUs of each type of beer. Graph it.
# 
# Put the highest at the top, and the missing ones at the bottom.
# 
# - Tip: Look at the options for `sort_values` to figure out the `NaN` thing. The `?` probably won't help you here.

# In[26]:


df.groupby('Style').IBUs.median().sort_values(na_position='first').plot(kind='barh', figsize=(15, 20))


# ## Hmmmm, it looks like they are generally different styles. What are the most common 5 styles of high-IBU beer vs. low-IBU beer?
# 
# - *Tip: You'll want to think about it in three pieces - filtering to only find the specific beers beers, then finding out what the most common styles are, then getting the top 5.*
# - *Tip: You CANNOT do this in one command. It's going to be one command for the high and one for the low.*
# - *Tip: "High IBU" means higher than 75th percentile, "Low IBU" is under 25th percentile*

# In[27]:


df[df.IBUs > 64].Style.value_counts().head(5)


# In[28]:


df[df.IBUs < 21].Style.value_counts().head(5)


# ## Get the average IBU of "Witbier", "Hefeweizen" and "American Pale Wheat Ale" styles
# 
# I'm counting these as wheat beers. If you see any other wheat beer categories, feel free to include them. I want ONE measurement and ONE graph, not three separate ones. And 20 to 30 bins in the histogram, please.
# 
# - *Tip: I hope that `isin` is in your toolbox*

# In[29]:


wheat_beers = ["Witbier", "Hefeweizen", "American Pale Wheat Ale"]

df[df.Style.isin(wheat_beers)].IBUs.mean()


# ## Draw a histogram of the IBUs of those beers

# In[30]:


df[df.Style.isin(wheat_beers)].IBUs.hist(bins=25)


# ## Get the average IBU of any style with "IPA" in it (also draw a histogram)

# In[31]:


df[df.Style.str.contains('IPA', na=False)].IBUs.mean()


# In[32]:


df[df.Style.str.contains('IPA', na=False)].IBUs.hist(bins=25)


# ## Plot those two histograms on top of one another
# 
# To plot two plots on top of one another, you *might* just be able to plot twice in the same cell. It depends on your version of pandas/matplotlib! If it doesn't work, you'll need do two steps.
# 
# 1. First, you make a plot using `plot` or `hist`, and you save it into a variable called `ax`.
# 2. You draw your second graph using `plot` or `hist`, and send `ax=ax` to it as a parameter.
# 
# It would look something like this:
# 
# ```python
# ax = df.plot(....)
# df.plot(ax=ax, ....)
# ``` 
# 
# And then youull get two plots on top of each other. They won't be perfect because the bins won't line up without extra work, but it's fine!

# In[33]:


df[df.Style.str.contains('IPA', na=False)].IBUs.hist(bins=25)
df[df.Style.isin(wheat_beers)].IBUs.hist(bins=25)


# ## Compare the ABV of wheat beers vs. IPAs : their IBUs were really different, but how about their alcohol percentage?
# 
# Wheat beers might include witbier, hefeweizen, American Pale Wheat Ale, and anything else you think is wheaty. IPAs probably have "IPA" in their name.

# In[34]:


df[df.Style.str.contains('IPA', na=False)].ABV.hist(bins=25)
df[df.Style.isin(wheat_beers)].ABV.hist(bins=25)


# ## Good work!
# 
# For making it this far, your reward is my recommendation for Athletic Brewing Co.'s products as the best non-alcoholic beer on the market. Their Run Wild IPA and Upside Dawn are both very solid.

# In[ ]:




