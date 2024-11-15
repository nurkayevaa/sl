import streamlit as st
import pandas as pd
import datetime
import oracledb
from sqlalchemy import create_engine

# CSS to hide the deploy button
st.set_page_config(page_title="Excel Download")

st.markdown("""
    <style>
        .reportview-container {
            margin-top: -2em;
        }
        #MainMenu {visibility: hidden;}
        .stAppDeployButton {display:none;}
        footer {visibility: hidden;}
        #stDecoration {display:none;}
    </style>
""", unsafe_allow_html=True)

# Constants
alllst = ["", " ", "_", "All", None, "Past 3 Years"]
month_replace = {
    1: "JAN", 2: "FEB", 3: "MAR", 4: "APR", 5: "MAY", 6: "JUN",
    7: "JUL", 8: "AUG", 9: "SEP", 10: "OCT", 11: "NOV", 12: "DEC"
}

import getpass
import oracledb
import streamlit as st
import csv
import pandas as pd
import datetime
from sqlalchemy import create_engine



alllst = [""," ","_", "All", None, "Past 3 Years"]

month_replace = {1:"JAN", 2:"FEB",3:"MAR", 4: "APR",5: "MAY",6:"JUN",\
                7:"JUL", 8:"AUG",9:"SEP", 10: "OCT",11:"NOV",12:"DEC"}
col1, col2, col3, col4 = st.columns(4)

fund = ""
department =""
fund_class = ""
vendor =""
unit = ""
reporting = ""
revenue = ""
object_cd = ""
subrev = ""
subobj = ""
doccd=""
refdoc = ""
docdept = ""
docid=""
refdocid=""
bsacc = ""
pst = ""
taskorder = ""
program = ""
mjprogram = ""
begdate = ""
enddate = ""
amt = ""
amtgt = ""
bankacc = ""
actcode =""
bfy =""
comm =""
group =""
event = ""
refdocdept = ""

varlst =[fund,
fund_class,
department, 
vendor, 
unit,
reporting ,
revenue ,
object_cd, 
subrev,
subobj , 
doccd, 
refdoc ,
docdept ,
refdocdept,
refdocid,
docid, 
bsacc ,
pst ,
taskorder ,
program ,
mjprogram ,
begdate ,
enddate ,
amt ,
amtgt ,
bankacc ,
actcode ,
bfy ,
comm ,
group , 
event]

# Field labels:
txtlst = """ Fund:	
Fund Class:	
Department:	
Vendor Customer Code:	
Unit Code:	
Reporting Code:	
Revenue Code:	
Object Code:	
Sub-Revenue Code:	
Sub-Object Code:	
Doc Cd:	
Ref Doc Cd:	
Doc Dept Cd:	
Ref Doc Dept:	
Doc Id:	
Ref Doc Id:	
Balance Sheet Account:	
Psting Code:	
Task Order Code:	
Program Code:	
Major Program Code:	
Beginning Date:	
Ending Date:	
Amount:	
Amount Greater than:	
Bank Acct Code:	
Activity Code:	
Budget Fiscal Year:	
Commodity Code:	
Group Code:	
Event Type:
 """.split('\n')
# table columns that filters refer to
fieldlst = ["FUND_CD", "FCLS_CD","DEPT_CD", "VEND_CUST_CD" , "UNIT_CD", "RPT_CD", "RSRC_CD",\
            "OBJ_CD", "SRSRC_CD", "SOBJ_CD", "DOC_CD", "RFED_DOC_CD", "DOC_DEPT_CD",\
            "RFED_DOC_DEPT_CD", "DOC_ID", "RFED_DOC_ID", "BSA_CD",  "PSTNG_CD_ID", \
            "TASK_ORD_CD", "PROG_CD", "MJR_PROG_CD", "DATEOFREC","DATEOFREC", "PSTNG_AM",\
            "PSTNG_AM","BANK_ACCT_CD", "ACTV_CD", "BFY", "COMM_CD", "GP_CD", "EVNT_TYP_ID", ] 

sqlwheres = """ """
#creating widgets 
def create_field(i,k):
    
    sqland=""" """
    sqland = """ """ if i  in alllst else """ And  """+k+""" = \'""" + str(i) +"""\'"""
    return sqland
#putting widgets in several cols 
def generate_sql_filters(sqland, datatype, yaeropt, begdate, enddate):
    and_datatype = f"AND type = '{datatype.upper()}'" if datatype not in alllst else ""
    year_conditions = {
        "Past 3 Years": "AND FY_DC > 2022",
        "Past 5 Years": "AND FY_DC > 2020",
        "All": ""
    }
    and_yearlst = f"AND FY_DC = '{yaeropt}'" if yaeropt not in year_conditions else year_conditions[yaeropt]
    and_begdate = f"AND DATEOFREC >= '{begdate.day}-{month_replace[begdate.month]}-{begdate.year}'"
    and_enddate = f"AND DATEOFREC <= '{enddate.day}-{month_replace[enddate.month]}-{enddate.year}'"
    return f"{and_datatype} {and_yearlst} {and_begdate} {and_enddate} {sqland}"





engine = create_engine('oracle+oracledb://', creator=lambda: connection)


with st.form("my_form"):
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        datatype = st.selectbox(
            "Data type",
            ("EXPENSE", "Revenue",  "Encumbrance", "Pre Encumbrance", "All"),
        )
        print(datatype)
    with col3:
        #st.write("You selected:", datatype)
        begdate = st.date_input("Beginning Date", datetime.date(2019, 7, 6))
    


    today = datetime.datetime.now()
    with col2:  
        yearlst = ["2025", "2024",  "2023", "Past 3 Years","Past 5 Years", "All"]  
        yaeropt = st.selectbox(
            "Year",
            (yearlst),
        )
        #st.write("You selected:", yaeropt)
        #st.write("You selected:", datatype)
    with col4:
        enddate = st.date_input("Ending Date", "today")

    
    for i,j,k in zip(varlst, txtlst,fieldlst):
        
        if txtlst.index(j)%4== 0:
            print(txtlst.index(j), txtlst.index(j))
            with col1:
                i = st.text_input(j, "_")
                #st.write("The current "+j, "all" if i in alllst else i )
                sqland = create_field(i,k)
                
                
                sqlwheres+= sqland
        elif txtlst.index(j)%4== 1:
            with col2:
                i = st.text_input(j, "_")
                sqland = create_field(i,k) 
                sqlwheres+= sqland
        elif txtlst.index(j)%4== 2:
            with col3:
                i = st.text_input(j, "_")
                sqland=""" """
                sqland = create_field(i,k)
                
                sqlwheres+= sqland
        elif txtlst.index(j)%4== 3:
            with col4:
                sqland=""" """
                i = st.text_input(j, "_")
                #st.write("The current "+j, "all" if i in alllst else i )
                sqland = """ """ if i  in alllst else """ And   \'"""+k+"""\' = """ + str(i) 
                sqlwheres+= sqland
    for i,j,k in zip(i, j,k):
        print(i,j,k)
    st.write( sqlwheres )
    # Every form must have a submit button.
    submitted = st.form_submit_button("Submit")



# Create query with filters
sqlwhere = generate_sql_filters(sqlwheres,datatype, yaeropt, begdate, enddate)

# Execute query and load data
if submitted:
    try:


        


        connection = oracledb.connect(
            user="ams_finadm", 
            password="CinsyOra1",
            dsn="cfsdbdev19.coc.ads:1521/fintrng")

        print("Successfully connected to Oracle Database")

        cursor = connection.cursor() 
       
        engine = create_engine('oracle+oracledb://', creator=lambda: connection)
        query = f"SELECT * FROM CIN_WF_EXCELDWNLD WHERE 1=1 {sqlwhere}"
        st.write(query)
        df = pd.read_sql(query, engine)
        st.write("Data fetched successfully.")
        @st.cache_data
        def convert_df(df):
            return df.to_csv(index=False).encode("utf-8")

        csv = convert_df(df)
        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name=f"{yaeropt}_{datatype}.csv",
            mime="text/csv"
        )
    except Exception as e:
        st.error("Database connection failed. Please check your credentials.")

        # Display data and provide download option
        if not df.empty:
            st.write(df)
            
            # CSV Download
            @st.cache_data
            def convert_df(df):
                return df.to_csv(index=False).encode("utf-8")

            csv = convert_df(df)
            st.download_button(
                label="Download data as CSV",
                data=csv,
                file_name=f"{yaeropt}_{datatype}.csv",
                mime="text/csv"
            )
        else:
            st.write("No data found.")

