import requests
import streamlit as st
import sqlite3

def get_city (origin, destination):
    url = f"https://api.codebazan.ir/distance/index.php?type=json&mabda={origin}&maghsad={destination}"
    try:
        respoonse = requests.get(url)
        if respoonse.status_code != 200 :
            return'page not finde'
        else:
            respoonse = respoonse.json()
            result = respoonse['result']
            return result
    except requests.RequestException:
        return None 

con = sqlite3.connect('masafat.db')
cursor = con.cursor()

sql_creat_table = ''' CREATE TABLE IF NOT EXISTS cities 
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  origin TEXT,destination TEXT,
                  distance INTEGER)
                              '''
cursor.execute(sql_creat_table)
con.commit()

def insert(origin, destination, distance):
    cursor.execute('INSERT INTO cities (origin, destination, distance) VALUES (?,?,?)',(origin, destination, distance))
    con.commit()

def delete(id):
    cursor.execute('DELETE FROM cities WHERE id = ?', (id,))
    con.commit()

def delete_all():
    cursor.execute('DELETE FROM cities')
    con.commit()

def read_where1(origin):
    cursor.execute('SELECT * FROM cities WHERE origin = ?', (origin,))
    return cursor.fetchall()

def read_where2(destination):
    cursor.execute('SELECT * FROM cities WHERE destination = ?', (destination,))
    return cursor.fetchall()

def read_where3(id):
    cursor.execute('SELECT * FROM cities WHERE id = ?', (id,))
    return cursor.fetchall()

def read_full():
    cursor.execute('SELECT * FROM cities')
    return cursor.fetchall()

st.sidebar.title('setting')
setting = st.sidebar.selectbox('diagrees', ('Distance','Delete from history','Delete all of history','searched origin',
                                            'searched destination','Make table','About us'))

if setting == 'Distance':
    st.title('Welcom to your Website')
    st.write('How far is it from you to anywhere in Iran? We will tell you.')
    origin = st.text_input('Enter your first city (farsi) : ').strip()
    destination = st.text_input('Enter your second city (farsi) : ').strip()

    if origin and destination:
        result = get_city(origin ,destination)
        if result == None:
            st.error('Error : requests conection')
        elif result == 'page not finde':
            st.error('Error : please try again')
        elif result == 'مبدا و یا مقصد مورد نظر در لیست ما وجود ندارد':
            st.error('Error : Destination or origin is invalid')
        else:
            col1, col2, col3 = st.columns(3)
            col1.metric(f"Source :", f"{origin}")
            col2.metric(f"Destination :", f"{destination}")
            col3.metric(f"Distance :", f"{result} KM")
            if st.button('save'):    
                insert(origin, destination, result)
                st.success('insert table')
            

elif setting == 'Delete from history':
    st.title('Delete by ID')
    id = st.number_input("Enter ID:", min_value=1, step=1)
    if st.button("Delete"):
        results = read_where3(id)
        if results:
            delete(id)
            st.success(f'Record with ID {id} deleted')
        else:
            st.error(f'No record found with ID {id}')

elif setting == 'Delete all of history':
    st.title("Delete All History")
    if st.button("Confirm deletion"):
        delete_all()
        st.success("All records cleared")  

elif setting == 'searched origin':
    city1 = st.text_input('Enter city :')
    if st.button('search'):
        results = read_where1(city1)
        if results:
            st.dataframe(results, column_config={"0": "ID", "1": "origin", "2": "destination", "3": "Distance (KM)"})
        else:
            st.info("No records found")

elif setting == 'searched destination':
    city2 = st.text_input('Enter city :')
    if st.button('search'):
        results = read_where2(city2)
        if results:
            st.dataframe(results, column_config={"0": "ID", "1": "origin", "2": "destination", "3": "Distance (KM)"})
        else:
            st.info("No records found")

elif setting == 'Make table':
    st.title("world of weather")
    data = read_full()
    if data:
        st.dataframe(data, column_config=
                     {"0": "ID", "1": "origin", "2": "destination", "3": "Distance (KM)"})
    else:
        st.info("No records in database")

elif setting == 'About us':
    st.title('About This Project')
    st.write("This Streamlit project, developed by Iliya & It measures the distance between two cities for you.")
    st.title('Contact Us')

    st.write('you can contact us via :')
    col1 , col2 , col3 = st.columns(3)
    with col1 : 
        st.write('Telegram : @iliya_12344')
        st.link_button('Go to Telegram', 'https://t.me/iliya_12344')
    with col2 :
        st.markdown('Instagram : @iliyakh177')
        st.link_button('Go to Instagram', 'https://www.instagram.com/iliyakh177?igsh=dXpkNHM2OTl6OHho')
    with col3 :
        st.write('Email : iliyakh660@gmail.com')

