
# coding: utf-8

# ## AI for Medicine Course 3 Week 1 lecture notebook
# ## Logistic Regression Model Interpretation

# Welcome to this exercise! You'll review how to interpret the coefficients in a logistic regression model. 
#  - The logistic regression is considered a **Generalized Linear Model**. 
#  - In general, you would employ one of these models to interpret the relationship between variables. 
#  - The logistic regression can be interpreted in terms of the **odds** and **OR** (Odds Ratio), which you'll learn about here.

# ### Import Libraries

# In[1]:


# Import libraries that you will use in this notebook
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression


# ### Load the Data

# In[2]:


# Read in the data
data = pd.read_csv("dummy_data.csv", index_col=0)

# View a few rows of the data
data.head()


# Here is a description of all the fields:
# 
# - `sex (binary): 1 if Male, 0 if Female`
# - `age (int): age of patient at the beginning of the study`
# - `obstruct (binary): obstruction of colon by tumor`
# - `outcome (binary): 1 if patient died within 5 years`
# - `TRTMT (binary): if patient was treated`
# 
# You'll want to pay close attention to the `TRTMT` and `outcome` columns. 
# - `TRTMT`: Whether a treatment is effective, and how effective it is for particular patients, is what you are interested in determining from a random control trial.
# - `outcome`: To measure the effective of treatment, you'll have the 5-year survival rate.  This is stored in the `outcome` variable, which is a binary variable with two possible values.  1 indicates that the patient died, and 0 indicates that the patient did not die during the 5-year period.

# ### Logistic regression
# 
# The formula for computing a logistic regression has the following form:
# 
# $$\sigma(\theta^T x^{(i)}) = \frac{1}{1 + e^{\left(-\theta^T x^{(i)}\right)}},$$
# 
# $x^{(i)}$ refers to example 'i' (a particular patient, or generally, a single row in a data table).
# 
# $\theta^T x^{(i)} = \sum_{j} \theta_j x^{(i)}_j$ is the linear combination of the features $x_1^{(i)}$, $x_2^{(i)}$, $x_2^{(i)}$ etc., weighted by the coefficients $\theta_1$, $\theta_2$, $\theta_3$ etc.
# 
# So for this example, $\theta^T x^{(i)} = \theta_{TRTMT} x^{(i)}_{TRTMT} + \theta_{AGE}x_{AGE}^{(i)} + \theta_{SEX}x^{(i)}_{SEX}$
# 
# Also, $\sigma$ is the sigmoid function, defined as $\sigma(a) = \frac{1}{1 + e^{(-a)}}$ for some variable $a$.  The output of the sigmoid function ranges from 0 to 1, so it's useful. in representing probabilities (whose values also range from 0 to 1).
# 
# If $x^{(i)}$ is the input vector and $OUTCOME$ is the target variable, then $\sigma(\theta^T x^{(i)})$ models the probability of death within 5 years.
# 
# For example, if the data has three features, $TRTMT$, $AGE$, and  $SEX$, then the patient's probability of death is estimated by: 
# 
# $$Prob(OUTCOME=1) = \sigma(\theta^T x^{(i)}) = \frac{1}{1 + e^{\left(-\theta_{TRTMT} x^{(i)}_{TRTMT} - \theta_{AGE}x_{AGE}^{(i)} - \theta_{SEX}x^{(i)}_{SEX}\right)}}$$

# ### Fit the Model
# 
# Let's separate the data into the target variable and the features and fit a logistic regression to it. Notice that in this case you are **not separating the data into train and test sets** because you're interested in the **interpretation of the model**, not its predictive capabilities.

# In[ ]:


# Get the labels
y = data.outcome

# Get the features (exclude the label)
X = data.drop('outcome', axis=1)

# Fit the logistic regression on the features and labels
classifier = LogisticRegression(solver='lbfgs').fit(X, y)


# ### Odds
# Looking at the underlying equation, you can't interpret the model in the same way as with a regular linear regression.
# - With a linear regression such as $y = 2x$ if the $x$ increases by 1 unit, then $y$ increases by 2 units.
# - How do you interpret the coefficient of a logistic regression model now that there is a sigmoid function?
# 
# Let's introduce the concept of **odds**, and you'll see how this helps with the interpretation of the logistic regression.
# 
# If an outcome is binary (either an event happens or the event doesn't happen):
# - Let $p$ represent the probability of the event (such as death).
# - Let $1-p$ represent the probability that the event doesn't happen (no death).
# - The odds are the probability of the event divided by 1 minus the probability of the event:
# 
# $$\mathrm{odds} = \frac{p}{1-p}$$
# 
# Going back to the logistic regression, recall that the sigmoid function $\sigma$ ranges between 0 and 1, and so it's a useful function for representing a probability.
# - So, let $p$, the probability of event, be estimated by $\sigma(\theta^T x^{(i)})$.
# 
# The **odds** defined in terms of the probability of an event $p$ are:
# 
# $$\mathrm{odds} = \frac{p}{1 - p}$$
# 
# Substitute $p = \sigma(\theta^T x^{(i)})$ to get:
# $$\mathrm{odds} = \frac{\sigma(\theta^T x)}{1 - \sigma(\theta^T x)}$$
# 
# Substitute for the definition of sigmoid: $\sigma(\theta^T x^{(i)}) = \frac{1}{1 + e^{(-\theta^T x)}}$
# $$\mathrm{odds} = \frac{\frac{1}{1 + e^{(-\theta^T x)}}}{1 - \frac{1}{1 + e^{(-\theta^T x)}}} $$
# 
# Multiply top and bottom by $1 + e^{(-\theta^T x)}$ and simplify to get:
# $$\mathrm{odds} = \frac{1}{\left ( 1 + e^{(-\theta^T x)} \right)  - (1)}$$
# 
# Do some more cleanup to get:
# $$\mathrm{odds} = e^{\left(\theta^T x^{(i)}\right)}$$
# 
# So what is this saying?
# - The odds (probability of death divided by probability of not death) can be estimated using the features and their coefficients if you take the dot product of the coefficients and features, then exponentiate that dot product (take e to the power of the dot product).
# 
# Since working with the exponential of something isn't necessarily easier to think about, you can take one additional transformation to get rid of the exponential, coming up next.

# ### Logit
# 
# Note that the inverse function of exponentiation is the natural log
# - $\mathrm{log}(e^{a}) = a$
# - $e^{(\mathrm{log}(a))} = a$
# 
# So if you want to "remove" the exponential $e$, you can apply the natural log function, which we'll write as $\mathrm{log}$.  You may have seen natural log written as $\mathrm{ln}$ as well, but we'll use $\mathrm{log}$ because Python functions usually name natural log functions as `log`.
# 
# Note that the log of odds is defined as the **logit** function:
# $$\mathrm{logit}(a) = \mathrm{log}\frac{a}{1-a}$$
# 
# Apply the $\mathrm{log}()$ to the odds:
# 
# $$\text{logit} = \log(\text{odds}) = \log\left(\frac{p}{1 - p}\right)= \log\left( e^{\left(\theta^T x^{(i)}\right)}\right) = \theta^T x^{(i)}$$
# 
# So, what's nice about this?
# - The right side of this equation is now a weighted sum of the features in $x^{(i)}$, weighted by coefficients in $\theta^T$.
# 

# ### Interpreting the coefficient's effect on the logit
# 
# This is an improvement in the interpretability of your model. 
# - Now you can interpret a single coefficient $\theta_j$ in a similar way that you interpret the coefficient in regular linear regression.
# 
# For a small example, let's say the coefficient for age is 0.2, patient A has age=40, and the logit for patient A is 3.
# $$\text{logit} = \theta_{age} \times x_{age} + \cdots $$
# 
# Patient A (now)  
# $$ 3 = \theta_{age} \times 40 + \cdots $$
# 
# If you increase patient A's age by 1 year, then this increases the logit by 0.2 (which is the coefficient for age).  
# Patient (A one year older):
# $$ 3 + 0.2 = 0.2 \times (40 + 1) + \cdots $$
# 
# 

# ### The range of possible values for the logit
# A nice feature of the logit (log odds) is the range of possible values it can have. The $\mathrm{logit}$ function can be any real number between $-\infty$ and $+\infty$.
# 
# One way to see this is to look at the ranges of values for the sigmoid, the odds, and then logit.
# - The sigmoid $\sigma(a)$ ranges from 0 to 1 for a variable $a$.  Recall that we're letting $p = \sigma(a)$
# - The odds $\frac{p}{1-p}$ can be as small as 0 (when $p=0$) and as large as $+\infty$ (when $p \rightarrow \infty$).  So the odds range from 0 to $+\infty$.
# - $\mathrm{log}(\mathrm{odds})$ can range from $-\infty$ (when the odds are 0), to $+\infty$ (when the odds approach $+\infty$).  
# - So the range of the log odds is $-\infty$ to $+\infty$
# 
# To check the coefficients of the model, you can use the model's `coef_ attribute`.

# In[5]:


# Get the coefficients (the thetas, or weights for each feature)
thetas = classifier.coef_
thetas


# This will return a numpy array containing the coefficient for each feature variable. Let's print it in a nicer way:

# In[6]:


# Print the name of the feature and the coefficient for each feature
for i in range(len(X.columns)):
    print("Feature {:<9s}: coefficient = {:<10f}".format(X.columns[i], thetas[0, i]))


# The coefficient for age is `0.046`.  This means that when the `age` variable increases by one, the logit will increase in `0.046`. 

# ### Odds ratio
# 
# In order to fully leverage the information that the odds provide, there's one more very useful concept:
# the **"Odds Ratio"**, which we will write as OR for short.
# 
# The OR allows you to compare the odds of one situation versus another (by dividing one odds by another odds).
# 
# When computing the OR for binary variables, it's defined as the odds when the variable is 1 divided by the odds when the variable is 0. For example:
# 
# $$OR_{TRTMT} = \frac{\text{odds}(TRTMT=1)}{\text{odds}(TRTMT=0)}$$
# 
# In contrast, when computing the OR for continuous variables, it's defined as the ratio between the odds of the variable plus one unit and the odds of the variable. For example:
# 
# $$OR_{age} = \frac{\text{odds}(age+1)}{\text{odds}(age)}$$
# 
# For both cases, after applying the appropriate algebra to the formula, you should find that the **OR** for a variable is equal to $e$ to the power of the coefficient associated with it.
# 
# $$OR_{x_j} = e^{\theta_j}$$
# 
# Let's try it for the variable $AGE$:
# 
# $$OR_{age} = \frac{odds(age+1)}{odds(age)} = \frac{e^\left(\theta_{INTERCEPT} + \theta_{SEX}x^{(i)}_{SEX} + \theta_{AGE}(1+x_{AGE}^{(i)}) + \theta_{OBSTRUCT}x_{OBSTRUCT}^{(i)} + \theta_{TRTMT} x^{(i)}_{TRTMT}\right)}{e^\left(\theta_{INTERCEPT} + \theta_{SEX}x^{(i)}_{SEX} + \theta_{AGE}x_{AGE}^{(i)} + \theta_{OBSTRUCT}x_{OBSTRUCT}^{(i)} + \theta_{TRTMT} x^{(i)}_{TRTMT}\right)} = e^{\theta_{AGE}}$$
# 
# <br>
# 
# The case for binary variables is quite similar. You can see the derivation for the binary variable `TRTMT` in this week's graded assignment.
# 
# Now, let's compute the ORs for the feature variables:

# ### Compute the Odds Ratios

# In[7]:


# Compute Odds Ratios for each feature
odds_ratios = np.exp(thetas)
odds_ratios


# In[8]:


# Display the coefficient and odds ratio for each feature
for i in range(len(X.columns)):
    print("Feature {:<10s}: coefficient = {:<10f} // OR = {:.2f}".format(X.columns[i], thetas[0, i], odds_ratios[0, i]))


# ### Interpret Odds Ratio
# 
# - The features with a negative coefficient has an Odds Ratio that is smaller than 1 
# - and features with non-negative coefficients have ORs greater than 1.
# 
# A negative coefficient (like treatment) indicates that the feature `TRTMT` reduces the outcome (reduces risk of death), but it's not easy to interpret how much the coefficient value of `-0.419` actually reduces the risk of death.
# 
# However, now that you have calculated the Odds Ratio of `0.66` for `TRTMT`, you can interpret this value:
# - If the patient does not receive treatment, and let's assume that their odds of dying is some value like 2.
# - If the patient **does** receive treatment, then the patient's the odds of dying is $0.66 \times 2$.
# - In other words, the odds of dying if given treatment is 0.66 times the odds of dying if not receiving treatment.
# 
# As you can see from the Odds Ratios, the give data indicates that the following reduce risk of death:
# - Receiving treatment
# - Not presenting a colon obstruction
# - Being of younger age
# - Being male.

# **Congratulations on finishing this notebook!** By now, you should have a clearer understanding of how to interpret a Logistic Regression model as well as a better intuition for odds and odd ratios. **Great job!**
# 
