import pandas as pd
import streamlit as st

from freediving_analysis import collect_data_aida


index_event = int(st.number_input('Index event (Indique le nombre XXXX dans https://www.aidainternational.org/Events/EventDetails-XXXX de l\'événement)', value=3765, step=1))
# st.write('The current number is ', index_event)

if index_event :
    infos = collect_data_aida.get_details_event(index_event)
    
    html_string = "<h3>this is an html string</h3>"

    st.markdown(f"<h3> {infos['Title Event']}</h3>", unsafe_allow_html=True)   
    st.markdown(f"<h4> Start date: {infos['Start date']}</h4>", unsafe_allow_html=True)
    txt_dis = infos['Disciplines'] if 'Disciplines' in infos else ''
    st.markdown(f"<h4> Disciplines: {infos['Disciplines']}</h4>", unsafe_allow_html=True)  

    type_results = st.radio(
    "",
    ('StartList', 'Results'))

    days = collect_data_aida.get_days_competition(index_event, type_results)
    inv_days = {v: k for k, v in days.items()}

    options_day = st.multiselect(
        'Selectionne le ou les jours',
        inv_days)

        # st.write('You selected:', options_day)

    # df = .collect_data_aida.get_days_competition(index_event)
    dict_day = {}
    txt_day = ''
    for day_index in options_day :
        dict_day[inv_days[day_index]] = day_index
        txt_day = txt_day + '_' + inv_days[day_index]

    if len(dict_day) > 0 :  
        # st.write(dict_day)        
        df = collect_data_aida.get_results_event_list_days(index_event, dict_day, type_results)

        st.dataframe(df, hide_index=True)

        @st.cache_data
        def convert_df(df):
            # IMPORTANT: Cache the conversion to prevent computation on every rerun
            return df.to_csv(index=False).encode('utf-8')

        csv = convert_df(df)
        
        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name=f'aida_{type_results}_{index_event}_{txt_day}.csv',
            mime='text/csv',
        )

# with st.form("my_form"):
#     st.write("Inside the form")
    

    # for day in days :
        
    # if genre == 'Comedy':
    #     st.write('You selected comedy.')
    # else:
    #     st.write("You didn\'t select comedy.")
#     collect_data_aida.
# df = collect_data_aida.get_results_events([3, 3449])
    

#    # Every form must have a submit button.
#    submitted = st.form_submit_button("Submit")
#    if submitted:
#        st.write("slider", slider_val, "checkbox", checkbox_val)

# st.write("Outside the form")
