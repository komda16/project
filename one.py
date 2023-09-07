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
