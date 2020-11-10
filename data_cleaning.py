import data_scraping as ds
import pandas as pd

df = ds.scrape_jobs("data scientist", 1000, False, "/Users/devpatel/PersonalProjects/chromedriver", 15)

df['hourly'] = df['Salary Estimate'].apply(lambda x: 1 if 'per hour' in x.lower() else 0)
df['employer_provided'] = df['Salary Estimate'].apply(lambda x: 1 if 'employer provided salary:' in x.lower() else 0)

df = df[df['Salary Estimate']!='-1']

Salary = df['Salary Estimate'].apply(lambda x: x.split('(')[0])
minus_kd = Salary.apply(lambda x: x.replace('K','').replace('$',''))

min_hr = minus_kd.apply(lambda x: x.lower().replace('per hour','').replace('employer provided salary:',''))

df['min_salary'] = min_hr.apply(lambda x: int(x.split('-')[0]))

df['max_salary'] = min_hr.apply(lambda x: int(x.split('-')[1]))

df['average_salary'] = (df.min_salary + df.max_salary)/2

df['company_text'] = df.apply(lambda x: x['Company Name'] if x['Rating'] <0 else x['Company Name'][:-3], axis = 1)

df['States'] = df['Location'].apply(lambda x: x.split(',')[1])
df['States'].value_counts()
df['Same State'] = df.apply(lambda x: 1 if x.Location == x.Headquarters else 0, axis = 1)

df['age'] = df['Founded'].apply(lambda x: x if x < 1 else 2020 - x)

df['Python'] = df['Job Description'].apply(lambda x: 1 if 'python' in x.lower() else 0)

df['R_Studio'] = df['Job Description'].apply(lambda x: 1 if 'R-studio' in x.lower() or 'R studio' in x.lower() else 0)

df['Tableau'] = df['Job Description'].apply(lambda x: 1 if 'Tableau' in x.lower() else 0)

df['Spark'] = df['Job Description'].apply(lambda x: 1 if 'Spark' in x.lower() else 0)

df['Excel'] = df['Job Description'].apply(lambda x: 1 if 'excel' in x.lower() else 0)

df['aws'] = df['Job Description'].apply(lambda x: 1 if 'aws' in x.lower() else 0)

df.drop(['Unnamed: 0'], axis=1, inplace=True)

df #checking out the df


###########################--------- Feature Engineering ---------###########################


def title_simplifier(title):
    if 'data scientist' in title.lower():
        return 'data scientist'
    elif 'data engineer' in title.lower():
        return 'data engineer'
    elif 'analyst' in title.lower():
        return 'analyst'
    elif 'machine learning' in title.lower():
        return 'mle'
    elif 'manager' in title.lower():
        return 'manager'
    elif 'director' in title.lower():
        return 'director'
    else:
        return 'na'
    
def seniority(title):
    if 'sr' in title.lower() or 'senior' in title.lower() or 'sr' in title.lower() or 'lead' in title.lower() or 'principal' in title.lower():
            return 'senior'
    elif 'jr' in title.lower() or 'jr.' in title.lower():
        return 'jr'
    else:
        return 'na'

df['job_simp'] = df['Job Title'].apply(title_simplifier)

df['seniority'] = df['Job Title'].apply(seniority)

df['job_state']= df.job_state.apply(lambda x: x.strip() if x.strip().lower() != 'los angeles' else 'CA')

df['desc_len'] = df['Job Description'].apply(lambda x: len(x))

df['num_comp'] = df['Competitors'].apply(lambda x: len(x.split(',')) if x != '-1' else 0)

df['min_salary'] = df.apply(lambda x: x.min_salary*2 if x.hourly ==1 else x.min_salary, axis =1)
df['max_salary'] = df.apply(lambda x: x.max_salary*2 if x.hourly ==1 else x.max_salary, axis =1)

df['company_txt'] = df.company_txt.apply(lambda x: x.replace('\n', ''))


df.to_csv('DS_salary_data.csv')

