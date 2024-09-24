# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customie Your Smoothies :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom smoothie!
    """
)

session = get_active_session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

name_on_order = st.text_input('Name on smoothie:')
ingredient_list = st.multiselect('Choose up to 5 ingrediants:', my_dataframe, 
                                 max_selections = 5)

ingredient_string = ''
if ingredient_list:
    for ingredient in ingredient_list:
        ingredient_string += ingredient + ' '
    # st.text(ingredient_string)

    time_to_submit = st.button('Submit Order')
    
    if time_to_submit:
        my_insert_stmt = """
                        insert into smoothies.public.orders (INGREDIENTS, name_on_order)
                        values ('""" +ingredient_string +"""',  '"""+ name_on_order+"""')
                    """
        # st.write(my_insert_stmt)
        sql = session.sql(my_insert_stmt).collect()
        st.success("""Your smoothie is ordered, '"""+ name_on_order+"""'""")
        st.stop()


    
