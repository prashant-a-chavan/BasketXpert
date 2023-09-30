import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
from mlxtend.frequent_patterns import association_rules, apriori, fpgrowth
import base64

ourColor = "#6ba4ff"


#favicon set
st.set_page_config(page_title="BasketXpert", page_icon="favi4.jpeg", layout="centered", initial_sidebar_state="auto", menu_items=None)



#hide streamlit water mark
hide_streamlit_style = """
            <style>
            [data-testid="stToolbar"] {visibility: hidden !important;}
            footer {visibility: hidden !important;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

#starting witdh of side bar injected
st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            width: 300px !important; # Set the width to your desired value
        }
    </style>
    """,
    unsafe_allow_html=True,
)





# helper function to read the csv files
def funDataset(file_path):
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        return None
st.set_option('deprecation.showPyplotGlobalUse', False)

st.title("BasketXpert's Dashboard!")

tab = st.sidebar.selectbox("Select Tab", ["BasketXpert", "Upload File", "Descriptive Data Analytics", "Prescriptive Data Analytics"])

if tab == "BasketXpert":
    st.write("BasketXpert data analysis")
elif tab == "Upload File":
    st.write("Upload your transaction file below")
    #  implementing file upload functionality using Streamlit's file_uploader
    # making day, hour, month as new column to perform visulization
    uploaded_file = st.file_uploader("Upload file", type=["csv"])
    if uploaded_file:
        dataset = pd.read_csv(uploaded_file)
        st.subheader("Uploaded transaction Data:")
        st.write("Data Size :", dataset.shape[0] ,"rows and ",dataset.shape[1], " columns")
        st.dataframe(dataset.head())
        dataset['date_time'] = pd.to_datetime(dataset['date_time'])
        dataset["day"] = dataset['date_time'].dt.weekday
        dataset["month"] = dataset['date_time'].dt.month
        dataset['hour'] = dataset['date_time'].dt.hour
        st.session_state['dataset'] = dataset #storing data(csv file) in variable dataset with session start


elif tab == "Descriptive Data Analytics":
    st.sidebar.subheader("Choose a Chart")
    chart = st.sidebar.selectbox("Select a Chart", ["Popular Order Times", "All About Reorders", "Purchasing Behaviour"])

    if chart == "Popular Order Times":
        st.subheader("Popular Order Times")
        # Implementing the Popular Order Times plot using Plotly
        if 'dataset' in st.session_state:
            dataset = st.session_state['dataset']
            if 'date_time' in dataset.columns:#checking is date_time in dataset
                # dataset['date_time'] = pd.to_datetime(dataset['date_time'], format="%d-%m-%Y %H:%M")
                # dataset["month"] = dataset['date_time'].dt.month
                data_perbulan = dataset['month'].value_counts().sort_index()

                # Create a list of months with corresponding labels
                months_labels = [
                    ("January", 1),
                    ("February", 2),
                    ("March", 3),
                    ("April", 4),
                    ("May", 5),
                    ("June", 6),
                    ("July", 7),
                    ("August", 8),
                    ("September", 9),
                    ("October", 10),
                    ("November", 11),
                    ("December", 12)
                ]

                # list comprehension filter the months with values and their corresponding labels
                months_with_values = [(label, month) for label, month in months_labels if month in data_perbulan.index]

                # Extract months for plotting
                plot_months = [month for _, month in months_with_values]

                # Create a dictionary with months as keys and their corresponding values
                data_dict = {label: data_perbulan.get(month, 0) for label, month in months_with_values}

                # Set Streamlit title
                st.title("Total Transactions Every Month")

                # Plot the data using Streamlit
                plt.figure(figsize=(8, 5))
                sns.barplot(x=list(data_dict.keys()), y=list(data_dict.values()), color="#D5AAD3")
                plt.xticks(size=12, rotation=-30)
                plt.title("Total Transactions Every Month", size=16)
                st.pyplot()  # Display the plot

            else:
                st.write("Uploaded transaction should have column 'date_time' to visualise popular order time")
        
        
            st.write("<hr>",unsafe_allow_html=True)
            if 'dataset' in st.session_state:
                dataset = st.session_state['dataset']
                if 'date_time' in dataset.columns:
                    st.title("Total Transactions Every Day")
                    # dataset['date_time'] = pd.to_datetime(dataset['date_time'])
                    # dataset["day"] = dataset['date_time'].dt.weekday
                    data_perhour = dataset.groupby("day")["Transaction"].count()
                    plt.figure(figsize=(12, 6))
                    # Create the bar plot
                    sns.set_style("whitegrid")
                    sns.barplot(
                        x=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                        y=data_perhour.values, color="#BFFCC6"
                        )
                    # Customize the appearance of the plot
                    plt.xlabel('Days', size=15)
                    plt.ylabel('No of Orders', size=15)
                    plt.title('Number of Orders each Day', size=17)
                    plt.xticks(size=13)
                    # Display the plot using Streamlit
                    st.pyplot(plt) 
    
    
                else:
                    st.write("Uploaded transaction should have column 'date_time' to visualise popular order time")
    
    
            st.write("<hr>",unsafe_allow_html=True)
            if 'dataset' in st.session_state:
                dataset = st.session_state['dataset']
                if 'date_time' in dataset.columns:
                    st.title("Total Transactions Each Hour")
                    # dataset['date_time'] = pd.to_datetime(dataset['date_time'])
                    # dataset['hour'] = dataset['date_time'].dt.hour
                    data_perhour = dataset.groupby("hour")["Transaction"].count()
        
                    # Create a new figure for the bar plot with a specified size
                    plt.figure(figsize=(12, 6))
                    # Create the bar plot
                    sns.set_style("whitegrid")
                    sns.barplot(
                        x=data_perhour.index,
                        y=data_perhour.values, color="#24ffec"
                    )
                    # Customize the appearance of the plot
                    plt.xlabel('Hour', size=15)
                    plt.ylabel('No ofOrders', size=15)
                    plt.title('Number of Orders each Hour', size=17)
                    plt.xticks(size=13)
                    # Display the plot using Streamlit
                    st.pyplot(plt)   


        else:
            st.write("Please upload a transaction file in the 'Upload File' option.")


        

    elif chart == "All About Reorders":
        st.subheader("All About Reorders")
        # TODO: Implement the All About Reorders plots using Plotly
        if 'dataset' in st.session_state:
            data = st.session_state['dataset']
            data['is_reorder'] = data['Transaction'].duplicated(keep='first').astype(int)

            # Filter data to get only the reorder items
            reorder_items = data[data['is_reorder'] == 1]['Item']

            # Calculate and plot the most reordered items
            most_reordered_items = reorder_items.value_counts().head(10)  # Select the top 10 most reordered items
            plt.figure(figsize=(10, 8))
            sns.barplot(y=most_reordered_items.values, x=most_reordered_items.index, palette="viridis")
            plt.title("Top 10 Most Reordered Items", size=16)
            plt.xlabel("Count", size=12)
            plt.ylabel("Item", size=12)
            plt.tight_layout()
            st.pyplot()  # Display the plot
        else:
            st.write("Please upload a transaction file in the 'Upload File' option.")
    

    elif chart == "Purchasing Behaviour":
        if 'dataset' in st.session_state:
            st.write('10 Most Purchased Items')
            data = st.session_state['dataset']
            # Most purchased items
            plt.figure(figsize=(13, 5))
            sns.set_palette("muted")
            sns.barplot(x=data["Item"].value_counts()[:10].index, y=data["Item"].value_counts()[:10].values,color=ourColor)
            plt.xlabel("Items", size=15); plt.ylabel("sold", size=15)
            plt.xticks(size=13, rotation=45)
            plt.title('10 Most Purchased Items', size=17)
            st.pyplot(plt)


        # Group data by period of the day and item, count transactions, and sort
        
        # Group data by period of the day and item, count transactions, and sort
            data_period_day = data.groupby(['period_day', 'Item'])['Transaction'].count().reset_index().sort_values(['period_day', 'Transaction'], ascending=False)
            days = ['Morning', 'Afternoon', 'Evening', 'Night']

            # Create a new figure with subplots for each period of the day
            for day_period in days:
                st.write("<hr>",unsafe_allow_html=True)
                st.write(f"Top 10 Most Ordered Items in {day_period} : ")
                plt.figure(figsize=(12, 6))
                data_temp = data_period_day[data_period_day["period_day"] == day_period.lower()].head(10)
                sns.barplot(x=data_temp["Item"], y=data_temp["Transaction"],color=ourColor)
                plt.xlabel("Transaction Count", size=12)
                plt.ylabel("Item", size=12)
                plt.title(f"Top 10 Most Ordered Items in {day_period}", size=16)
                plt.tight_layout()
                st.pyplot()  # Display the plot
        else:
            st.write("Please upload a transaction file in the 'Upload File' option.")

elif tab == "Prescriptive Data Analytics":
       data = st.session_state['dataset']

       st.subheader("Apriori Algorithm")
 
       

       st.markdown('<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">', unsafe_allow_html=True)

       with open("style.css") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
        
        st.markdown(
        """
        <nav class="navbar fixed-top navbar-expand-lg navbar-dark" >
          <a href="/" target="_self" id="main-btn">Market Basket Analysis</a>
          <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
          </button>
          <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav"">
              <li class="nav-item">
                <a id="notebook" class="nav-link active" href="https://www.kaggle.com/code/danielsimamora/market-basket-analysis" target="_blank">📄Notebook</a>
              </li>
            </ul>
          </div>
        </nav>
        """, unsafe_allow_html = True)
        
        st.markdown("""<p id="title-1z2x">Bakery Shop Item Recommender</p>""", unsafe_allow_html=True)
        st.markdown("""<p id="caption-1z2x">A Web App that helps recommend items to customer!</p>""", unsafe_allow_html=True)
        
        # Processing the CSV as Pandas DataFrame
        data_depl = data
        data_depl['date_time'] = pd.to_datetime(data_depl['date_time'], format = "%d-%m-%Y %H:%M")
        
        data_depl["month"] = data_depl['date_time'].dt.month
        data_depl["day"] = data_depl['date_time'].dt.weekday
        
        data_depl["month"].replace([i for i in range(1, 12 + 1)], ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"], inplace = True)
        data_depl["day"].replace([i for i in range(6 + 1)], ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], inplace = True)

        # Filter the data based on User Inputs
        def get_data(period_day = '', weekday_weekend = '', month = '', day = ''):
            data = data_depl.copy()
            filtered = data.loc[
                (data["period_day"].str.contains(period_day)) & 
                (data["weekday_weekend"].str.contains(weekday_weekend)) & 
                (data["month"].str.contains(month.title())) &
                (data["day"].str.contains(day.title()))
            ]
            return filtered if filtered.shape[0] else "No result!"
        
        st.sidebar.header('User Input')
        st.sidebar.text("Use these widgets to input values")
        
        def user_input_features():
            # item = st.sidebar.selectbox("Item", ['Bread', 'Scandinavian', 'Hot chocolate', 'Jam', 'Cookies', 'Muffin', 'Coffee', 'Pastry', 'Medialuna', 'Tea', 'Tartine', 'Basket', 'Mineral water', 'Farm House', 'Fudge', 'Juice', "Ella's Kitchen Pouches", 'Victorian Sponge', 'Frittata', 'Hearty & Seasonal', 'Soup', 'Pick and Mix Bowls', 'Smoothies', 'Cake', 'Mighty Protein', 'Chicken sand', 'Coke', 'My-5 Fruit Shoot', 'Focaccia', 'Sandwich', 'Alfajores', 'Eggs', 'Brownie', 'Dulce de Leche', 'Honey', 'The BART', 'Granola', 'Fairy Doors', 'Empanadas', 'Keeping It Local', 'Art Tray', 'Bowl Nic Pitt', 'Bread Pudding', 'Adjustment', 'Truffles', 'Chimichurri Oil', 'Bacon', 'Spread', 'Kids biscuit', 'Siblings', 'Caramel bites', 'Jammie Dodgers', 'Tiffin', 'Olum & polenta', 'Polenta', 'The Nomad', 'Hack the stack', 'Bakewell', 'Lemon and coconut', 'Toast', 'Scone', 'Crepes', 'Vegan mincepie', 'Bare Popcorn', 'Muesli', 'Crisps', 'Pintxos', 'Gingerbread syrup', 'Panatone', 'Brioche and salami', 'Afternoon with the baker', 'Salad', 'Chicken Stew', 'Spanish Brunch', 'Raspberry shortbread sandwich', 'Extra Salami or Feta', 'Duck egg', 'Baguette', "Valentine's card", 'Tshirt', 'Vegan Feast', 'Postcard', 'Nomad bag', 'Chocolates', 'Coffee granules ', 'Drinking chocolate spoons ', 'Christmas common', 'Argentina Night', 'Half slice Monster ', 'Gift voucher', 'Cherry me Dried fruit', 'Mortimer', 'Raw bars', 'Tacos/Fajita'])

            unique_items = data_depl['Item'].unique()
            item = st.sidebar.selectbox("Item", unique_items)
            period_day = st.sidebar.selectbox('Period Day', ['Morning', 'Afternoon', 'Evening', 'Night'])
            weekday_weekend = st.sidebar.selectbox('Weekday / Weekend', ['Weekend', 'Weekday'])
            month = st.sidebar.select_slider("Month", ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
            day = st.sidebar.select_slider('Day', ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], value="Sat")
        
            return period_day, weekday_weekend, month, day, item
        
        period_day, weekday_weekend, month, day, item = user_input_features()
        
        data = get_data(period_day.lower(), weekday_weekend.lower(), month, day)
        
        st.text("")
        st.text("")
        try:
          st.text("User Input Dataframe:")
          st.dataframe(data)
        except:
          st.markdown("""<h4 style="text-align: center;">No transactions were done with that values 😕</h4>""", unsafe_allow_html=True)
        #   st.markdown("""
        #     <div id="ifno-result">
        #       <p>Here are some input values to give a try!</p>
        #       <ul style="margin: 0 auto">
        #         <li>Period Day: &nbsp;<i>Morning</i></li>
        #         <li>Weekday/Weekend: &nbsp;<i>Weekend</i></li>
        #         <li>Month: &nbsp;<i>Jan</i></li>
        #         <li>Day: &nbsp;<i>Sun</i></li>
        #       </ul>
        #     </div>
        #   """, unsafe_allow_html=True)
        
        
        # ==========================================================================================================================================================================
        
        def encode(x):
            if x <= 0:
                return 0
            elif x >= 1:
                return 1
        
        if type(data) != type("No result!"):
          item_count = data.groupby(["Transaction", "Item"])["Item"].count().reset_index(name = "Count")
          item_count_pivot = item_count.pivot_table(index='Transaction', columns='Item', values='Count', aggfunc='sum').fillna(0)
          item_count_pivot = item_count_pivot.applymap(encode)
        
          support = 0.01 # atau 1%
          frequent_items = apriori(item_count_pivot, min_support = support, use_colnames = True)
        
          metric = "lift"
          min_threshold = 1
        
          rules = association_rules(frequent_items, metric = metric, min_threshold = min_threshold)[["antecedents", "consequents", "support", "confidence", "lift"]]
          rules.sort_values('confidence', ascending = False, inplace = True)
        
        def parse_list(x):
            x = list(x)
            if len(x) == 1:
                return x[0]
            elif len(x) > 1:
                return ", ".join(x)
            
        def return_item_df(item_antecedents):
            data = rules[["antecedents", "consequents"]].copy()
            
            data["antecedents"] = data["antecedents"].apply(parse_list)
            data["consequents"] = data["consequents"].apply(parse_list)
            
            matching_rows = data.loc[data["antecedents"] == item_antecedents]
            
            if not matching_rows.empty:
                return list(matching_rows.iloc[0,:])
            else:
                return []
        
        # ...
        
        if type(data) != type("No result!"):
            st.text("")
            st.text("")
        
            if type(data) != type("No result!"):
                st.markdown("""<p id="recommendation-1z2x">Recommendation:</p>""", unsafe_allow_html=True)
                recommendations = return_item_df(item)
                if recommendations:
                    st.markdown(f"Customer who buys **{item}**, also buys **{recommendations[1]}**!")
                else:
                    st.markdown(f"No matching recommendations found for **{item}**!")
        
        
       
