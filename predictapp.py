import streamlit as st
import pickle
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

model = pickle.load(open('model.pkl','rb'))
le_country_code = pickle.load(open('le_country_code.pkl','rb'))
le_job_title = pickle.load(open('le_job_title.pkl','rb'))
le_employment_type = pickle.load(open('le_employment_type.pkl','rb'))
le_company_size = pickle.load(open('le_company_size.pkl','rb'))
le_remote_ratio = pickle.load(open('le_remote_ratio.pkl','rb'))

def predict_experience_level(work_year,job_title,employment_type,salary_in_usd,company_location, employee_residence	,company_size, remote_ratio):
    job_title_input = le_job_title.transform(np.array([job_title]))
    employment_type_input = le_employment_type.transform(np.array([employment_type]))
    company_size_input = le_company_size.transform(np.array([company_size]))
    remote_ratio_input = le_remote_ratio.transform(np.array([int(remote_ratio)]))
    employee_residence_input = le_country_code.transform(np.array([employee_residence]))
    company_location_input = le_country_code.transform(np.array([company_location]))

    input = np.array([[work_year,job_title_input,employment_type_input,salary_in_usd,company_location_input,employee_residence_input,company_size_input,remote_ratio_input]])
    prediction = model.predict(input)
    return prediction


def main():
    st.title("Experience Prediction")
    html_temp = """
    <div style="background:#025246 ;padding:10px">
    <h2 style="color:white;text-align:center;"> Experience Prediction ML App </h2>
    </div>
    """
    st.markdown(html_temp, unsafe_allow_html = True)

    Work_year = st.selectbox('Year of data',('2020', '2021', '2022'))
    Job_title = st.selectbox("Job Title",('Principal Data Engineer','Research Scientist','Financial Data Analyst','Applied Machine Learning Scientist','Principal Data Scientist','Data Scientist','Data Analytics Lead','Applied Data Scientist','Director of Data Science','Data Engineer','Lead Data Engineer','ML Engineer','Data Architect','Machine Learning Scientist','Machine Learning Engineer','Data Science Manager','Head of Data','Head of Data Science','Analytics Engineer','Director of Data Engineering','Data Analyst','AI Scientist','Machine Learning Infrastructure Engineer','Lead Data Scientist','Data Engineering Manager','Lead Data Analyst','Principal Data Analyst','Data Specialist','Cloud Data Engineer','Data Analytics Manager','BI Data Analyst','Computer Vision Software Engineer','Business Data Analyst','Data Science Engineer','Computer Vision Engineer','Machine Learning Manager','Big Data Engineer','Data Analytics Engineer','Staff Data Scientist','Data Science Consultant','Machine Learning Developer','Big Data Architect','Marketing Data Analyst','Lead Machine Learning Engineer','Head of Machine Learning','Finance Data Analyst','ETL Developer','NLP Engineer','Product Data Analyst','3D Computer Vision Researcher'))
    Employment_type = st.radio("Employment Type",('Contract', 'Freelance', 'Full-time','Part-time'))
    Salary_in_usd = st.number_input("Salary(in usd)",2000,700000,50000,10)
    Company_location = st.selectbox("Company Location",( 'US', 'JP', 'RU', 'CA', 'GB', 'DE', 'PL', 'FR', 'AU', 'NZ', 'CH', 'AE', 'IL', 'SI', 'IQ', 'CN', 'DZ', 'IN', 'AT', 'SG', 'DK', 'BE', 'ES', 'GR', 'IE', 'CZ', 'NL', 'LU', 'PT', 'RO', 'MX', 'IT', 'NG', 'HR', 'CL', 'MY', 'HU', 'EE', 'MT', 'TR', 'BR', 'CO', 'HN', 'PK', 'AS', 'MD', 'UA', 'KE', 'IR', 'VN'))
    Employee_residence = st.selectbox("Employee Residence",('US', 'JP', 'RU', 'MY', 'IN', 'CA', 'GB', 'DE', 'BR', 'PR', 'IT', 'AU', 'ES', 'NZ', 'CH', 'AE', 'SG', 'PL', 'SI', 'IQ', 'JE', 'DZ', 'FR', 'AT', 'GR', 'BE', 'NL', 'BG', 'RO', 'BO', 'IE', 'CZ', 'HK', 'PT', 'AR', 'LU', 'PK', 'NG', 'VN', 'DK', 'PH', 'HR', 'CN', 'CL', 'HU', 'MX', 'EE', 'TN', 'MT', 'TR', 'RS', 'CO', 'HN', 'MD', 'UA', 'KE', 'IR'))
    Company_size = st.radio("Company Size",('S', 'M', 'L'))
    Remote_ratio = st.radio("Remote Ratio",('0', '50', '100'))

    if Employment_type == 'Contract':
        Employment_type_input = 'CT'
    else:
        if Employment_type == 'Freelance':
            Employment_type_input = 'FL'
        else:
            if Employment_type == 'Full-time':
                Employment_type_input = 'FT'
            else:
                Employment_type_input = 'PT'

    safe_html ="""  
    <div style="background-color:#80ff80; padding:10px >
    <h2 style="color:white;text-align:center;"> The Abalone is young</h2>
    </div>
    """

    warn_html ="""  
    <div style="background-color:#F4D03F; padding:10px >
    <h2 style="color:white;text-align:center;"> The Abalone is middle aged</h2>
    </div>
    """
    danger_html="""  
        <div style="background-color:#F08080; padding:10px >
        <h2 style="color:black ;text-align:center;"> The Abalone is old</h2>
        </div>
    """

    if st.button("Predict experience"):
        output = predict_experience_level(Work_year,Job_title,Employment_type_input,Salary_in_usd,Company_location,Employee_residence,Company_size,Remote_ratio)
        st.success('The experience level is {}'.format(output))

        if output == 1:
            st.markdown(safe_html,unsafe_allow_html=True)
        elif output == 2:
            st.markdown(warn_html,unsafe_allow_html=True)
        elif output == 3:
            st.markdown(danger_html,unsafe_allow_html=True)

if __name__=='__main__':
    main()