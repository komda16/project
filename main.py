import streamlit
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import sqlite3
from streamlit_option_menu import option_menu
from st_aggrid import AgGrid,GridOptionsBuilder,ColumnsAutoSizeMode
import hashlib

conn=sqlite3.connect("church.db",check_same_thread=False)
conn.row_factory=lambda cursor,row: row[0]
cur=conn.cursor()


def add_user(a,b,c,d,e,f):
    cur.execute("CREATE TABLE IF NOT EXISTS user("
                "NAME TEXT,CONTACT TEXT,CHURCH TEXT,TITLE TEXT,USERNAME TEXT,PASSWORD TEXT);")
    cur.execute("INSERT INTO user VALUES(?,?,?,?,?,?)", (a, b, c, d,e,f))
    conn.commit()
    conn.close()
    st.success("successfully saved")
def addchurch(a,b,c,d):
    cur.execute("CREATE TABLE IF NOT EXISTS church(NAME TEXT,PASTOR TEXT,LAND TEXT,STRUCTURE TEXT);")
    cur.execute("INSERT INTO church VALUES(?,?,?,?)", (a, b, c, d))
    conn.commit()
    conn.close()
    st.success("successfully saved")


def add_finance(a,b,c,d,e):
    cur.execute("""CREATE TABLE IF NOT EXISTS finance(
    DATE TEXT,
    CHURCH TEXT,
    TITHE INT,
    OFFERTORY INT,
    SUNDAY_SCHOOL INT);""")
    cur.execute("INSERT INTO finance VALUES(?,?,?,?,?)", (a, b, c, d,e))
    conn.commit()
    conn.close()
    st.success("successfully saved")


def add_member(a, b, c, d, e, f):
    cur.execute("""CREATE TABLE IF NOT EXISTS member(
    NAME TEXT, CHURCH TEXT,CATEGORY TEXT,CONTACT TEXT,ADDRESS TEXT, SEX TEXT);""")
    cur.execute("INSERT INTO member VALUES(?,?,?,?,?,?)", (a, b, c, d, e, f))
    conn.commit()
    conn.close()
    st.success("successfully saved")


def add_inventory(a, b, c, d, e):
    cur.execute("""CREATE TABLE IF NOT EXISTS invent(DATE TEXT,CHURCH TEXT,ITEM TEXT,QUANTITY INT,CATEGORY TEXT);""")
    cur.execute("INSERT INTO invent VALUES(?,?,?,?,?)", (a, b, c, d, e))
    conn.commit()
    conn.close()
    st.success("successfully saved")


def user():
    with st.form("New User"):

        churc = cur.execute("SELECT name FROM church").fetchall()

        st.subheader("New User Form")
        churchn = st.selectbox("Church Name", churc)
        name = str.title(st.text_input("Name"))
        contact = st.text_input("Contact")
        user = str.title(st.text_input("User Name"))
        passw = hashlib.sha256(str.encode(st.text_input("Password"))).hexdigest()
        title = st.selectbox("Category",["Assembly Pastor","Associate Pastor"])
        sub_butto = st.form_submit_button(label="Save")

        if sub_butto == True:
            add_user(name, contact,churchn, title, user,passw)


def inventory():
    with st.form("Inventory"):
        conn.row_factory = lambda cursor, row: row[0]

        churc = cur.execute("SELECT name FROM church").fetchall()

        st.subheader("Inventory Form")
        date = st.date_input("Date")
        churchn = st.selectbox("Church Name", churc)
        item = str.title(st.text_input("Item"))
        cate = str.title(st.text_input("Category"))
        quat = str.title(st.text_input("Quantity"))
        sub_butto = st.form_submit_button(label="Save")

        if sub_butto == True:
            add_inventory(date, churchn, item, quat, cate)



def finance():
    st.markdown("""<style>[data-testid='stMetric value']{font-size:100px}<style>""", unsafe_allow_html=True)
    with st.form("Finance"):

        churc = cur.execute("SELECT name FROM church")

        st.subheader("Finance Form")
        date=st.date_input("Date")
        churchn=st.selectbox("Church Name",churc)
        tithe=st.text_input("Tithe")
        offertory = st.text_input("Offertory")
        sunday= st.text_input("Sunday School")
        sub_butto = st.form_submit_button(label="Save")

        if sub_butto == True:
            add_finance(date,churchn,tithe,offertory,sunday)


def dash_bord():

    st.subheader("P.A.G ANAKA ASSEMBLY")
    side1, col5, col6, col7,sid1,sid2 = st.columns([0.5, 1, 1, 1, 1, 1])

    with col5:

        da = cur.execute("""SELECT DISTINCT name FROM church""")
        cols = [column[0] for column in da.description]
        fra = pd.DataFrame(da, columns=cols)

        tc = fra['NAME'].count()
        st.metric(label="CHURCHES", value=tc)

    with col6:
        cur.row_factory=None

        ta = cur.execute("""SELECT*FROM member""")
        col = [column[0] for column in ta.description]
        df = pd.DataFrame(ta, columns=col)

        to = df['CHURCH'].value_counts(dropna=True)

        tab = cur.execute("""SELECT*FROM member""")
        cols = [column[0] for column in tab.description]
        fd = pd.DataFrame(tab, columns=cols)

        tot = fd['NAME'].count()
        bark = fd['CATEGORY'].value_counts()
        st.metric(label="TOTAL CHRISTIANS", value=tot)



    with col7:

        dav = cur.execute("""SELECT category FROM member WHERE category LIKE 'a%'""")
        cols = [column[0] for column in dav.description]
        frame = pd.DataFrame(dav, columns=cols)

        tc = frame['CATEGORY'].count()
        st.metric(label="ADULTS",value=tc)

    with sid1:

        dav = cur.execute("""SELECT category FROM member WHERE category LIKE 'c%'""")
        cols = [column[0] for column in dav.description]
        frame = pd.DataFrame(dav, columns=cols)

        tc = frame['CATEGORY'].count()
        st.metric(label="CHILDREN",value=tc)

    with sid2:

        dav = cur.execute("""SELECT category FROM member WHERE category LIKE 'y%'""")
        cols = [column[0] for column in dav.description]
        frame = pd.DataFrame(dav, columns=cols)

        tc = frame['CATEGORY'].count()
        st.metric(label="YOUTH",value=tc)

    col8, col9 = st.columns([ 2, 3])
    with col8:
        st.markdown("")
        st.markdown("")
        st.markdown("")
        st.markdown("")

        cha = to.plot(kind='pie',autopct=lambda x:'{:.0f}'.format(x*to.sum()/100))
        # to display chart
        st.pyplot(plt.gcf())

    with col9:
        st.markdown("")
        tab = cur.execute("""SELECT*FROM member""")
        cols = [column[0] for column in tab.description]
        datas = pd.DataFrame(tab, columns=cols)

        fig = px.bar(datas, x='CHURCH',color='CATEGORY',barmode='group',height=400, width=400, color_discrete_sequence=px.colors.qualitative.D3)
        st.write(fig)


def new_member():
    with st.form(key="form1"):
        col1,col2=st.columns([0.5,1])
        with col1:
            names=str.title(st.text_input("Name"))
            gender=["Male","Female"]
            sex=st.selectbox("Sex",gender)
            address=str.title(st.text_input("Address"))
            sub_but = st.form_submit_button(label="Save")

        with col2:
            cat=["Adult","Youth","Child"]
            chu=cur.execute("SELECT NAME FROM church")
            category=str.title(st.selectbox("Category",cat))
            church =str.title( st.selectbox("Church", chu))
            contact=st.text_input("Contact")
        if sub_but == True:
            add_member(names, church, category, contact, address, sex)


def table():
    cols1,cols2=st.columns([1,4])

    with cols1:

        we=["Members","Add Member","Delete"]
        choices=st.radio("MENU",we)

    with cols2:
        if choices=='Members':
            cur.row_factory = None
            tab1 = cur.execute("""SELECT*FROM member""")
            cols = [column[0] for column in tab1.description]
            fdr = pd.DataFrame(tab1,columns=cols)
            AgGrid(fdr,
                   gridOptions=GridOptionsBuilder.from_dataframe(fdr).build(),
                   columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS
            )
        if choices=='Add Member':
            new_member()
        if choices=='Delete':
            delete_member()


def table1():

    cur.row_factory=None
    tab1=cur.execute("""SELECT*FROM church""")
    cols = [column[0] for column in tab1.description]
    fdr=pd.DataFrame(tab1,columns=cols)
    AgGrid(fdr,
           gridOptions=GridOptionsBuilder.from_dataframe(fdr).build(),
           columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS
           )


def invent():

    cur.row_factory=None
    tab1=cur.execute("""SELECT*FROM invent""")
    cols = [column[0] for column in tab1.description]
    fdr=pd.DataFrame(tab1,columns=cols)
    AgGrid(fdr.head(7),
           gridOptions=GridOptionsBuilder.from_dataframe(fdr).build(),
           columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS
           )


def delete_user():
    la=st.text_input("User Name",placeholder="Enter the Username to be Deleted")
    but=st.button("DELETE")
    cur.execute("""DELETE FROM user WHERE username=?""",(la,))
    conn.commit()
    st.success('User Deleted')


def delete_member():
    la = str.title(st.text_input("Name",placeholder="Enter the Member to be Deleted"))
    but=st.button("DELETE")

    if but==True:
        cur.execute("""DELETE FROM member WHERE name=?""", (la,))
        conn.commit()
        st.success('Member Deleted')


def delete_church():
    la = str.title(st.text_input("Name"))
    but = st.button("DELETE")
    if but==True:
        cur.execute("""DELETE FROM church WHERE name=?""", (la,))
        conn.commit()
        st.success('Church Deleted')

def delete_invent():
    la = str.title(st.text_input("Item"))
    but = st.button("DELETE")
    if but==True:
        cur.execute("""DELETE FROM invent WHERE item=?""", (la,))
        conn.commit()
        st.success('Item Deleted')



def de_fin():

     ex = st.date_input("Date")
     butto = st.button("DELETE")
     lx = cur.execute('SELECT church FROM user WHERE username=?', (username,))
     if butto == True:
         cur.execute("""DELETE FROM finance WHERE date=? AND church=?""", (ex,lx))
         conn.commit()
         st.success('Entry Deleted')

def Church():

        choices=st.sidebar.selectbox("MENU",["Home","Finance","Members","Inventory"])
        if choices == 'Home':
            church_home()
            table1()
        if choices == 'Inventory':
            invent()
        if choices=='Finance':
            finance()
        if choices=='members':
            inventory()


def home_church():

    tab1 = cur.execute("""SELECT name FROM church""")
    # st.sidebar(tab1)
    global choice
    choice = st.selectbox('CHURCHES', tab1)


def church_page():
    st.markdown("""<style>[data-testid='stMetric value']{font-size:100px}<style>""", unsafe_allow_html=True)
    col1,col2=st.columns([1,5])
    with col1:
        home_church()
        lu=st.checkbox('Edit Churches')




    with col2:
        if lu==True:
            la=option_menu(menu_title=None,options=(['Delete Church','Add Church']),orientation='horizontal')
            if la=='Delete Church':
                delete_church()

            if la=='Add Church':
                new_church()

        st.subheader("  " + choice + "-" + "PAG Church")

        col6, col7, sid1, sid2 = col2.columns([ 1, 1, 1, 1])

        with col6:

            cur.row_factory = None
            ta = cur.execute("""SELECT*FROM member""")
            col = [column[0] for column in ta.description]
            df = pd.DataFrame(ta, columns=col)
            to = df['CHURCH'].value_counts()

            d = cur.execute("""SELECT*FROM member WHERE church=?""", (choice,))
            cols = [column[0] for column in d.description]
            fram = pd.DataFrame(d, columns=cols)

            tc = fram['NAME'].count()

            st.metric(label="TOTAL CHRISTIANS", value=tc)

        with col7:
            dav = cur.execute("""SELECT category FROM member WHERE category LIKE 'a%' AND church=?""", (choice,))
            cols = [column[0] for column in dav.description]
            frame = pd.DataFrame(dav, columns=cols)

            tc = frame['CATEGORY'].count()
            st.metric(label="ADULTS", value=tc)


        with sid1:

            dav = cur.execute("""SELECT category FROM member WHERE category LIKE 'c%' AND church=?""", (choice,))
            cols = [column[0] for column in dav.description]
            frame = pd.DataFrame(dav, columns=cols)

            tc = frame['CATEGORY'].count()
            st.metric(label="CHILDREN", value=tc)


        with sid2:
            dav = cur.execute("""SELECT category FROM member WHERE category LIKE 'y%' AND church=?""", (choice,))
            cols = [column[0] for column in dav.description]
            frame = pd.DataFrame(dav, columns=cols)

            tc = frame['CATEGORY'].count()
            st.metric(label="YOUTH", value=tc)
            cur.row_factory=lambda cursor,row:row[0]

    st.markdown("___")

    col1,col2=st.columns([1.5,4])

    with col1:
        choices = st.radio("", ['Finance', 'Inventory', 'Members'])
    with col2:

        if choices=='Members':


            tap=st.checkbox("Edit Member")
            if tap==True:
                pa=['Delete Member','Update Member','Add Member']
                lap=option_menu(menu_title=None,options=pa,orientation='horizontal')
                if lap=='Delete Member':
                    delete_member()
                if lap=='Add Member':
                    new_member()

            else:

                cur.row_factory = None
                tab1 = cur.execute("""SELECT*FROM member WHERE church=?""",(choice,))
                cols = [column[0] for column in tab1.description]
                fdr = pd.DataFrame(tab1, columns=cols)
                AgGrid(fdr,
                       gridOptions=GridOptionsBuilder.from_dataframe(fdr).build(),
                       columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS
                       )
        if choices=="Inventory":
            lu = st.checkbox('Edit Inventory')
            if lu == True:

                la =option_menu(menu_title=None,options=('Add Item', 'Delete Item'),orientation='horizontal')
                if la=='Add Item':
                    inventory()
                if la=='Delete Item':
                    delete_invent()
            else:
                dav = cur.execute("""SELECT*FROM invent WHERE church=?""", (choice,))
                cols = [column[0] for column in dav.description]
                frame = pd.DataFrame(dav, columns=cols)
                AgGrid(frame,
                       gridOptions=GridOptionsBuilder.from_dataframe(frame).build(),
                       columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS
                       )

        if choices=="Finance":
            col5, col6, sid1 = st.columns([2, 2, 2])

            with col5:
                da = cur.execute("""SELECT tithe AND offertory AND sunday_school FROM finance WHERE church=?""",
                                 (choice,))
                can = cur.execute("""SELECT DISTINCT date FROM finance""").fetchall()

                cols = [column[0] for column in da.description]
                fra = pd.DataFrame(da, columns=cols)
                global laps
                laps = st.selectbox('Period', can)


            with col6:
                cur.row_factory = None
                ta = cur.execute("""SELECT*FROM finance WHERE date=? AND church=?""", (laps, choice))
                col = [column[0] for column in ta.description]
                df = pd.DataFrame(ta, columns=col)

                to = sum(df['TITHE']) + sum(df['OFFERTORY']) + sum(df['SUNDAY_SCHOOL'])
                st.metric(label="__TOTAL COLLECTION__", value=to)

                dav = cur.execute("""SELECT*FROM finance WHERE date=? AND church=?""", (laps, choice))
                cols = [column[0] for column in dav.description]
                frame = pd.DataFrame(dav, columns=cols)
                st.markdown("""<style>[data-testid='stMetric value']{font-size:100px}<style>""", unsafe_allow_html=True)
                tc = sum(frame['TITHE'])
                st.metric(label="__TITHE__", value=tc)




            with sid1:
                dav = cur.execute("""SELECT*FROM finance WHERE date=? AND church=?""", (laps, choice))
                cols = [column[0] for column in dav.description]
                frame = pd.DataFrame(dav, columns=cols)

                tc = sum(frame['OFFERTORY'])
                st.metric(label="__OFFERTORY__", value=tc)

                dav = cur.execute("""SELECT*FROM finance WHERE date=? AND church=?""", (laps, choice))
                cols = [column[0] for column in dav.description]
                frame = pd.DataFrame(dav, columns=cols)

                tc = sum(frame['SUNDAY_SCHOOL'])
                st.metric(label="__SUNDAY SCHOOL__", value=tc)




            st.markdown('')
            tx=st.checkbox('Edit Finance')
            if tx==True:
                lx=option_menu(menu_title=None,options=('New Entry','Delete Entry'),orientation='horizontal')
                if lx=='New Entry':
                    cur.row_factory=lambda cursor,row:row[0]
                    finance()
                if tx=='Delete Entry':
                    finance()

            else:
                dav = cur.execute("""SELECT*FROM finance WHERE church=?""", (choice,))
                cols = [column[0] for column in dav.description]
                frame = pd.DataFrame(dav, columns=cols)
                AgGrid(frame,
                       gridOptions=GridOptionsBuilder.from_dataframe(frame).build(),
                       columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS
                       )






def church_home():
    home_church()


    st.subheader(choice + "-" + "PAG CHURCH")

    side1, col5, col6, col7, sid1, sid2 = st.columns([0.5, 1, 1, 1, 1, 1])


    with col6:
        cur.row_factory = None
        ta = cur.execute("""SELECT*FROM member""")
        col = [column[0] for column in ta.description]
        df = pd.DataFrame(ta, columns=col)
        # select column.
        # tut = df['CHURCH'].df['CATEGORY']
        to = df['CHURCH'].value_counts()

        d = cur.execute("""SELECT*FROM member WHERE church=?""", (choice,))
        cols = [column[0] for column in d.description]
        fram = pd.DataFrame(d, columns=cols)

        tc = fram['NAME'].count()

        st.metric(label="TOTAL CHRISTIANS", value=tc)

    with col7:
        dav = cur.execute("""SELECT category FROM member WHERE category LIKE 'a%' AND church=?""",(choice,))
        cols = [column[0] for column in dav.description]
        frame = pd.DataFrame(dav, columns=cols)

        tc = frame['CATEGORY'].count()
        st.metric(label="ADULTS", value=tc)

    with sid1:
        dav = cur.execute("""SELECT category FROM member WHERE category LIKE 'c%' AND church=?""",(choice,))
        cols = [column[0] for column in dav.description]
        frame = pd.DataFrame(dav, columns=cols)

        tc = frame['CATEGORY'].count()
        st.metric(label="CHILDREN", value=tc)

    with sid2:
        dav = cur.execute("""SELECT category FROM member WHERE category LIKE 'y%' AND church=?""",(choice,))
        cols = [column[0] for column in dav.description]
        frame = pd.DataFrame(dav, columns=cols)

        tc = frame['CATEGORY'].count()
        st.metric(label="YOUTH", value=tc)




def new_church():
    with st.form(key="form2"):
        lan =["Given","Bought"]
        struct=["Permanent","Temporary"]
        st.subheader("church Registration Form")
        church_name=str.title(st.text_input("Church Name"))
        associate_pastor=str.title(st.text_input("Associate Pastor"))
        land=str.title(st.selectbox("Land", lan))
        structure=str.title(st.selectbox("Structure", struct))
        sub_butt = st.form_submit_button(label="Save")
        if sub_butt == True:
            addchurch(church_name, associate_pastor, land, structure)
def run():
    st.title('PAG WEST ACHOLI PASTORATE')
    selected=st.sidebar.selectbox('MENU',["Home", "Churches","Finance", "Setting" ])


    if selected=="Home":
        dash_bord()
    if selected=="Churches":
        church_page()
    if selected=="Finance":
        finan_dash()
    if selected == "Setting":
        lax=st.checkbox('Edit User')
        if lax==True:
            lex=option_menu(menu_title=None,options=('Delete User','Add User'),orientation='horizontal')
            if lex=='Add User':
                user()
            if lex=='Delete User':
                delete_user()
        else:
            cur.row_factory = None
            tab1 = cur.execute("""SELECT*FROM user""")
            cols = [column[0] for column in tab1.description]
            fdr = pd.DataFrame(tab1, columns=cols)
            AgGrid(fdr,
                   gridOptions=GridOptionsBuilder.from_dataframe(fdr).build(),
                   columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS
                   )

def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()
def check_hashes(password,hashed_text):
    if make_hashes(password)==hashed_text:
        return hashed_text
    return False

def user_login(username,password):
    cur.execute('SELECT*FROM user WHERE username=? AND password=?',(username,password))
    data=cur.fetchall()
    return data

def view_user():
    cur.execute('SELECT church FROM user WHERE username=?', (username,)).fetchone()
    global lr
    lr=cur.fetchone()



def login():
    #hide_st_style ="""<style> #MainMenu {visibility: hidden;} footer {visibility: hidden;} <style>"""
    #st.markdown(hide_st_style, unsafe_allow_html=True)
    global username
    username=st.sidebar.text_input('User Name')
    password=st.sidebar.text_input('Password',type='password')
    if st.sidebar.checkbox('Login'):
        hashed_pswd=make_hashes(password)
        result=user_login(username,check_hashes(password,hashed_pswd))
        if result:
            fa=cur.execute('SELECT title FROM user WHERE username=?',(username,)).fetchone()
            if fa=='Assembly Pastor':
                run()
            if fa=='Associate Pastor':
                tas=cur.execute('SELECT church FROM user WHERE username=?',(username,)).fetchone()
                col1, col2 = st.columns([1, 5])


                with col2:
                    st.subheader("  " + tas + "-" + "PAG Church")

                c1, col6, col7, sid1, sid2 = st.columns([1, 1, 1, 1, 1])

                with col6:

                    cur.row_factory = None
                    ta = cur.execute("""SELECT*FROM member""")
                    col = [column[0] for column in ta.description]
                    df = pd.DataFrame(ta, columns=col)
                    # select column.
                    # tut = df['CHURCH'].df['CATEGORY']
                    to = df['CHURCH'].value_counts()

                    d = cur.execute("""SELECT*FROM member WHERE church=?""", (tas,))
                    cols = [column[0] for column in d.description]
                    fram = pd.DataFrame(d, columns=cols)

                    tc = fram['NAME'].count()

                    st.metric(label="TOTAL CHRISTIANS", value=tc)

                with col7:
                    dav = cur.execute("""SELECT category FROM member WHERE category LIKE 'a%' AND church=?""",
                                      (tas,))
                    cols = [column[0] for column in dav.description]
                    frame = pd.DataFrame(dav, columns=cols)

                    tc = frame['CATEGORY'].count()
                    st.metric(label="ADULTS", value=tc)

                with sid1:

                    dav = cur.execute("""SELECT category FROM member WHERE category LIKE 'c%' AND church=?""",
                                      (tas,))
                    cols = [column[0] for column in dav.description]
                    frame = pd.DataFrame(dav, columns=cols)

                    tc = frame['CATEGORY'].count()
                    st.metric(label="CHILDREN", value=tc)

                with sid2:
                    dav = cur.execute("""SELECT category FROM member WHERE category LIKE 'y%' AND church=?""",
                                      (tas,))
                    cols = [column[0] for column in dav.description]
                    frame = pd.DataFrame(dav, columns=cols)

                    tc = frame['CATEGORY'].count()
                    st.metric(label="YOUTHS", value=tc)
                    cur.row_factory = lambda cursor, row: row[0]

                st.markdown("___")

                col1, col2 = st.columns([0.5, 4])

                with col1:
                    choices = st.radio("", ['Members', 'Inventory', 'Finance'])
                with col2:

                    if choices == 'Members':

                        tap = st.checkbox("Edit Member")
                        if tap == True:
                            pa = ['Delete Member','Add Member']
                            lap = option_menu(menu_title=None, options=pa, orientation='horizontal')
                            if lap == 'Delete Member':
                                delete_member()
                            if lap == 'Add Member':
                                new_member()

                        else:

                            cur.row_factory = None
                            tab1 = cur.execute("""SELECT*FROM member WHERE church=?""", (tas,))
                            cols = [column[0] for column in tab1.description]
                            fdr = pd.DataFrame(tab1, columns=cols)
                            AgGrid(fdr,
                                   gridOptions=GridOptionsBuilder.from_dataframe(fdr).build(),
                                   columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS
                                   )
                    if choices == "Inventory":
                        lu = st.checkbox('Edit Inventory')
                        if lu == True:

                            la = option_menu(menu_title=None, options=('Add Item', 'Delete Item'),
                                             orientation='horizontal')
                            if la == 'Add Item':
                                inventory()
                            if la == 'Delete Item':
                                delete_invent()
                        else:
                            dav = cur.execute("""SELECT*FROM invent WHERE church=?""", (tas,))
                            cols = [column[0] for column in dav.description]
                            frame = pd.DataFrame(dav, columns=cols)
                            AgGrid(frame,
                                   gridOptions=GridOptionsBuilder.from_dataframe(frame).build(),
                                   columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS
                                   )

                    if choices == "Finance":
                        side1, col5, col6, sid1 = st.columns([0.1, 2, 2, 2])

                        with col5:
                            da = cur.execute(
                                """SELECT tithe AND offertory AND sunday_school FROM finance WHERE church=?""",
                                (tas,))
                            can = cur.execute("""SELECT DISTINCT date FROM finance WHERE church=?""",(tas,)).fetchall()

                            cols = [column[0] for column in da.description]
                            fra = pd.DataFrame(da, columns=cols)
                            global laps
                            laps = st.selectbox('Period', can)

                        with col6:
                            cur.row_factory = None
                            ta = cur.execute("""SELECT*FROM finance WHERE date=? AND church=?""", (laps, tas))
                            col = [column[0] for column in ta.description]
                            df = pd.DataFrame(ta, columns=col)

                            to = sum(df['TITHE']) + sum(df['OFFERTORY']) + sum(df['SUNDAY_SCHOOL'])
                            st.metric(label="__TOTAL COLLECTION__", value=to)

                            dav = cur.execute("""SELECT*FROM finance WHERE date=? AND church=?""", (laps, tas))
                            cols = [column[0] for column in dav.description]
                            frame = pd.DataFrame(dav, columns=cols)

                            tc = sum(frame['TITHE'])
                            st.metric(label="__TITHE__", value=tc)




                        with sid1:
                            dav = cur.execute("""SELECT*FROM finance WHERE date=? AND church=?""", (laps, tas))
                            cols = [column[0] for column in dav.description]
                            frame = pd.DataFrame(dav, columns=cols)

                            tc = sum(frame['OFFERTORY'])
                            st.metric(label="__OFFERTORY__", value=tc)

                            dav = cur.execute("""SELECT*FROM finance WHERE date=? AND church=?""", (laps, tas))
                            cols = [column[0] for column in dav.description]
                            frame = pd.DataFrame(dav, columns=cols)

                            tc = sum(frame['SUNDAY_SCHOOL'])
                            st.metric(label="__SUNDAY SCHOOL__", value=tc)




                        st.markdown('')
                        tx = st.checkbox('Edit Finance')
                        if tx == True:
                            lx = option_menu(menu_title=None, options=('New Entry', 'Delete Entry'),
                                             orientation='horizontal')
                            if lx == 'New Entry':
                                cur.row_factory = lambda cursor, row: row[0]
                                finance()
                            if lx == 'Delete Entry':

                                cur.row_factory = lambda cursor, row: row[0]

                                ex=st.date_input("Date")
                                butto = st.button("DELETE")
                                # lr = cur.execute('SELECT church FROM user WHERE username=?', (username,)).fetchone()
                                if butto == True:
                                    view_user()
                                    cur.execute("""DELETE FROM finance WHERE date=? AND church=?""", (ex, lr))
                                    conn.commit()

                                    st.success('Entry Deleted')



                        else:
                            dav = cur.execute("""SELECT*FROM finance WHERE church=?""", (tas,))
                            cols = [column[0] for column in dav.description]
                            frame = pd.DataFrame(dav, columns=cols)
                            AgGrid(frame,
                                   gridOptions=GridOptionsBuilder.from_dataframe(frame).build(),
                                   columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS
                                   )
    else:
        st.title('Praise King Jesus!: '
                 'May You Login Please At The Sidebar')

def finan_dash():
    st.subheader("P.A.G ANAKA ASSEMBLY")
    side1, col5, col6, col7, sid1, sid2 = st.columns([0.5, 2, 2, 2, 2, 2])

    with col5:
        da = cur.execute("""SELECT tithe AND offertory AND sunday_school FROM finance""")
        can=cur.execute("""SELECT DISTINCT date FROM finance""").fetchall()

        cols = [column[0] for column in da.description]
        fra = pd.DataFrame(da, columns=cols)
        global la
        la=st.selectbox('Period',can)


    with col6:
        cur.row_factory = None
        ta = cur.execute("""SELECT*FROM finance WHERE date=?""",(la,))
        col = [column[0] for column in ta.description]
        df = pd.DataFrame(ta, columns=col)

        to = sum(df['TITHE']) + sum(df['OFFERTORY']) + sum(df['SUNDAY_SCHOOL'])


        tab = cur.execute("""SELECT*FROM member""")
        cols = [column[0] for column in tab.description]
        fd = pd.DataFrame(tab, columns=cols)

        tot = fd['NAME'].count()
        bark = fd['CATEGORY'].value_counts()
        st.metric(label="__TOTAL COLLECTION__", value=to)

    with col7:
        dav = cur.execute("""SELECT*FROM finance WHERE date=?""",(la,) )
        cols = [column[0] for column in dav.description]
        frame = pd.DataFrame(dav, columns=cols)

        tc = sum(frame['TITHE'])
        st.metric(label="__TITHE__", value=tc)

    with sid1:
        dav = cur.execute("""SELECT*FROM finance WHERE date=?""",(la,))
        cols = [column[0] for column in dav.description]
        frame = pd.DataFrame(dav, columns=cols)

        tc = sum(frame['OFFERTORY'])
        st.metric(label="__OFFERTORY__", value=tc)

    with sid2:
        dav = cur.execute("""SELECT*FROM finance WHERE date=?""",(la,))
        cols = [column[0] for column in dav.description]
        frame = pd.DataFrame(dav, columns=cols)

        tc = sum(frame['SUNDAY_SCHOOL'])
        st.metric(label="__SUNDAY SCHOOL__", value=tc)

    col8, col9 = st.columns([0.1, 3])

    with col9:
        st.markdown("")
        tab = cur.execute("""SELECT*FROM finance WHERE date=?""",(la,))
        cols = [column[0] for column in tab.description]
        datas = pd.DataFrame(tab, columns=cols)

        fig = px.bar(data_frame=datas, x='CHURCH', y=["TITHE","OFFERTORY","SUNDAY_SCHOOL"], barmode='group',opacity=0.9,orientation="v"
                     )
        st.write(fig)

def inven_dash():
    home_church()

    lu=st.checkbox('Edit Inventory')
    if lu==True:

        col1,col2=st.columns([1,4])
        with col1:
            la=st.radio('',['Add Item','Delete Item'])
        with col2:
            if la=='Add Item':
                inventory()
    else:
        dav = cur.execute("""SELECT*FROM invent WHERE church=?""", (choice,))
        cols = [column[0] for column in dav.description]
        frame = pd.DataFrame(dav, columns=cols)
        AgGrid(frame,
               gridOptions=GridOptionsBuilder.from_dataframe(frame).build(),
               columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS
               )


def church_finance_dash():

    col5, col6,sid1,  = st.columns([ 2, 2, 2])
    with col5:
        da = cur.execute("""SELECT tithe AND offertory AND sunday_school FROM finance WHERE church=?""",(choice,))
        can = cur.execute("""SELECT DISTINCT date FROM finance""").fetchall()

        cols = [column[0] for column in da.description]
        fra = pd.DataFrame(da, columns=cols)
        global la
        la = st.selectbox('Period', can)

    with col6:
        cur.row_factory = None
        ta = cur.execute("""SELECT*FROM finance WHERE date=? AND church=?""", (la,choice))
        col = [column[0] for column in ta.description]
        df = pd.DataFrame(ta, columns=col)

        to = sum(df['TITHE']) + sum(df['OFFERTORY']) + sum(df['SUNDAY_SCHOOL'])
        st.metric(label="__TOTAL COLLECTION__", value=to)

        dav = cur.execute("""SELECT*FROM finance WHERE date=? AND church=?""", (la, choice))
        cols = [column[0] for column in dav.description]
        frame = pd.DataFrame(dav, columns=cols)

        tc = sum(frame['TITHE'])
        st.metric(label="__TITHE__", value=tc)

    with sid1:
        dav = cur.execute("""SELECT*FROM finance WHERE date=? AND church=?""", (la,choice))
        cols = [column[0] for column in dav.description]
        frame = pd.DataFrame(dav, columns=cols)

        tc = sum(frame['OFFERTORY'])
        st.metric(label="__OFFERTORY__", value=tc)

        dav = cur.execute("""SELECT*FROM finance WHERE date=? AND church=?""", (la, choice))
        cols = [column[0] for column in dav.description]
        frame = pd.DataFrame(dav, columns=cols)

        tc = sum(frame['SUNDAY_SCHOOL'])
        st.metric(label="__SUNDAY SCHOOL__", value=tc)



    st.metric('')

    dav = cur.execute("""SELECT*FROM invent WHERE church=?""", (choice,))
    cols = [column[0] for column in dav.description]
    frame = pd.DataFrame(dav, columns=cols)
    AgGrid(frame,
           gridOptions=GridOptionsBuilder.from_dataframe(frame).build(),
           columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS
           )
login()



