import dash
import dash_auth
from users import USERNAME_PASSWORD_PAIRS
from dash import dcc
from dash import html
import plotly
import dash_bootstrap_components as dbc
import dash_daq as dq
from jupyter_dash import JupyterDash
from dash import Dash
import pandas as pd  
import joblib
import base64, io, os
from dash import  dash_table
import dash
import pandas as pd
from dash import dash_table
import pickle
from dash.dependencies import Input, Output, State, ALL, MATCH
import json
from functools import reduce
from dash import Input, Output, State, html
from tqdm.notebook import trange, tqdm
import pickle
import numpy as np
import pandas as pd
from cryptography.fernet import Fernet
import json
import io, base64, os
import pandas as pd
import datetime
import time



class Encryptor():

    def key_create(self):
        key = Fernet.generate_key()
        return key

    def key_write(self, key, key_name):
        with open(key_name, 'wb') as mykey:
            mykey.write(key)

    def key_load(self, key_name):
        with open(key_name, 'rb') as mykey:
            key = mykey.read()
        return key


    def file_encrypt(self, key, original_file, encrypted_file):
        
        f = Fernet(key)

        original=pd.read_pickle(original_file)
                
        for k in original:
            f_ = io.BytesIO()
            original[k].columns = original[k].columns.astype(str)
            original[k]=original[k].astype(object)
            original[k].to_parquet(f_)
            f_.seek(0)
            original[k]=f.encrypt(f_.read())
            
        pd.to_pickle(original,encrypted_file)
            
    def load_decrypt(self, key, encrypted_file):
        
        f = Fernet(key)

        encrypted = pd.read_pickle(encrypted_file)

        decrypted = {}
        
        for k in encrypted:
            decrypted[k]=pd.read_parquet(io.BytesIO(f.decrypt(encrypted[k])))
        decrypted['ap_case_safe']['valid_int']=decrypted['ap_case_safe']['valid_int'].map(lambda x: datetime.datetime(2003, 6, 9)+datetime.timedelta(days=int(x)) if ~np.isnan(x) else np.nan)
        decrypted['ap_case_safe']['sub_int']=decrypted['ap_case_safe']['sub_int'].map(lambda x: datetime.datetime(2003, 6, 9)+datetime.timedelta(days=int(x)) if ~np.isnan(x) else np.nan)
        return decrypted

parent_directory="./data"    
encryptor=Encryptor()
loaded_key=encryptor.key_load(os.path.join(parent_directory,'path_db_v2.key'))
path_db=encryptor.load_decrypt(loaded_key, os.path.join(parent_directory,'text_db_encrypted_v2.pkl'))

data_dict = path_db
drop_down_menu_list = list(data_dict.keys())
all_chain_list = {}

PAGE_SIZE = 5

time.sleep(1000)

# with open('./Dendrite/search_dropdown_dict.txt', 'rb') as handle:
#     search_dropdown_dict = pickle.loads(handle.read())

# search_dropdown_datalist_list = []
# for one_table in list(data_dict.keys()):
#     for one_column in list(data_dict[one_table].columns):
#         append_name = 'datalist' + '_' + str(one_table) + '_' + str(one_column)
#         if one_column in ['id_safe', 'description', 'clin_hx_imp', 
#                           'ds_txt', 'flowdx', 'flowds', 'field_val', 
#                           'case_parts', 'clin_hxdx', 'pt_id_safe', 
#                           'txt', 'clin_hx_tx', 'gross', 
#                           'field_val', 'spc_from_dx', 'dx_txt_no_spc', 
#                           'dx_txt', 'mol_res_txt',]:
#             search_dropdown_datalist_list.append(html.Datalist(id=append_name,
#                                                   children=[], ),)
#         else:
#             search_dropdown_datalist_list.append(html.Datalist(id=append_name,
#                                                   children=[html.Option(value=l) for l in search_dropdown_dict[append_name]], ),)

            
# operators = [['ge ', '>='],
#              ['le ', '<='],
#              ['lt ', '<'],
#              ['gt ', '>'],
#              ['ne ', '!='],
#              ['eq ', '='],
#              ['contains '],
#              ['datestartswith ']]

# def Sorting(lst):
#     lst2 = sorted(lst, key=len, reverse = True)
#     return lst2

# def split_filter_part(filter_part):
#     for operator_type in operators:
#         for operator in operator_type:
#             if operator in filter_part:
#                 name_part, value_part = filter_part.split(operator, 1)
#                 name = name_part[name_part.find('{') + 1: name_part.rfind('}')]

#                 value_part = value_part.strip()
#                 v0 = value_part[0]
#                 if (v0 == value_part[-1] and v0 in ("'", '"', '`')):
#                     value = value_part[1: -1].replace('\\' + v0, v0)
#                 else:
#                     try:
#                         value = float(value_part)
#                     except ValueError:
#                         value = value_part

#                 # word operators need spaces after them in the filter string,
#                 # but we don't want these later
#                 return name, operator_type[0].strip(), value

#     return [None] * 3

# markdown_text_1 = '''
# # **Dendrite Demo**
# '''

# time.sleep(1000)


# filter_index_number = 1

# app = JupyterDash(__name__, external_stylesheets=[dbc.themes.SPACELAB])
# auth = dash_auth.BasicAuth(
#     app,
#     USERNAME_PASSWORD_PAIRS
# )

# SIDEBAR_STYLE = {
#     "position": "fixed",
#     "top": 0,
#     "left": 0,
#     "bottom": 0,
#     "width": "26rem",
#     "padding": "2rem 1rem",
#     "background-color": "#f8f9fa",
#     "overflow": "scroll",
# }

# CONTENT_STYLE = {
#     "margin-left": "28rem",
#     "margin-right": "2rem",
#     "padding": "2rem 1rem",
#     "display": "inline-block"
# }

# sidebar = html.Div(
#     search_dropdown_datalist_list + 
#     [
#         dcc.Markdown(children=markdown_text_1),
#         dbc.Button("Instructions", outline=True, 
#                    color="primary", className="me-1", size="sm", 
#                    id="open-offcanvas-scrollable",
#                    n_clicks=0,),
#         dbc.Offcanvas(
#             html.Div([
#             html.P("1. Add filters, select tables, columns and input keywords"),
#                 html.P("2. Input logic statement, like (1 AND (3 OR 2)). Use index according to Filter Info List. Use parentheses and capital AND, OR, NOT"),
#                 html.P("3. Select one or multiple tables you'd like to merge together"),
#                 html.P("4. Click Final Query, and use page flip function to see more rows"),
#                 html.P("5. Click Export button to export data from final query"),
#             ]),
#             id="offcanvas-scrollable",
#             placement = 'end',
#             scrollable=True,
#             title="Dendrite Instructions",
#             is_open=False,
#         ),
#         html.Hr(),
        
        
#         dbc.Button(
#                     "Add Filter",
#                     id="add-filter",
#                     n_clicks=0,
#                 ),
#         html.Div(id="container_1", children=[]),
#     ],
#     style=SIDEBAR_STYLE,
# )

# maindiv = html.Div([
#     html.H3('Filters info list:'),
#     html.H6(id="display_selected_values_2", 
#                 ),
#     dcc.Input(
#                     id="logic_input",
#                     placeholder="Filter logic", 
#                     debounce=True, 
#                 ),
#     dcc.Dropdown(
#                     id="final_input",
#         placeholder = 'Select Table(s)',
#             options = drop_down_menu_list,
#             multi=True,
#         ),
#     html.Br(),
#     dbc.Button(
#                     "Final Query",
#                     id="final-query",
#                     n_clicks=0,
#                 ),
#     dash_table.DataTable(id = "table", 
#                              columns = [],
#                              export_format="csv",
#                          style_as_list_view=True,
#                              style_table={'overflowX': 'auto', 'overflow': 'scroll', },
#                          style_cell_conditional=[
#                                                 {
#                                                     'if': {'column_id': c},
#                                                     'textAlign': 'left'
#                                                 } for c in ['Date', 'Region']
#                                             ],
#                                             style_data={
#                                                 'color': 'black',
#                                                 'backgroundColor': 'white'
#                                             },
#                                             style_data_conditional=[
#                                                 {
#                                                     'if': {'row_index': 'odd'},
#                                                     'backgroundColor': 'rgb(230, 230, 230)',
#                                                 }
#                                             ],
#                                             style_header={
#                                                 'backgroundColor': 'rgb(210, 210, 210)',
#                                                 'color': 'black',
#                                                 'fontWeight': 'bold'
#                                             },
#                             style_cell={
#                                 'height': 'auto',
#                                 'minWidth': '100px', 
#                                 'maxWidth': '1500px',
                                
#                                 'whiteSpace': 'normal'
#                             },
#                                  page_current=0,
#                                 page_size=PAGE_SIZE,
#                                 page_action='custom',

#                                 filter_action='custom',
#                                 filter_query='',

#                                 sort_action='custom',
#                                 sort_mode='multi',
#                                 sort_by=[]
#                             ),
#     ],
#     style=CONTENT_STYLE
# )

# @app.callback(
#     Output("offcanvas-scrollable", "is_open"),
#     Input("open-offcanvas-scrollable", "n_clicks"),
#     State("offcanvas-scrollable", "is_open"),
# )
# def toggle_offcanvas_scrollable(n1, is_open):
#     if n1:
#         return not is_open
#     return is_open

# @app.callback(
#     Output("container_1", "children"),
#     [
#         Input("add-filter", "n_clicks"),
#         Input({"type": "dynamic-delete", "index": ALL}, "n_clicks"),
#     ],
#     [State("container_1", "children"), 
#     ],
# )

# def display_filters(n_clicks, _, children, ):
#     input_id = dash.callback_context.triggered[0]["prop_id"].split(".")[0]
#     if "index" in input_id:
#         delete_chart = json.loads(input_id)["index"]
#         children = [
#             chart
#             for chart in children
#             if "'index': " + str(delete_chart) not in str(chart)
#         ]
#     else:
#         new_element = html.Div(
#             children=[
#                             html.Br(),
#                             dbc.Row(dbc.Col(dbc.Badge(
#                                     children = '  Filter ' + str(filter_index_number + n_clicks) + '  ',
#                                 id={"type": "filter_badge", "index": n_clicks},
#                                     color="white",
#                                     text_color="primary",
#                                     className="border me-1",
#                                     ))),
# #                             html.H6('  Filter ' + str(filter_index_number + n_clicks) + '  '),
#                             dbc.Row(dbc.Col(dbc.Button(
#                                                 "Remove",size="sm",
#                                                 id={"type": "dynamic-delete", "index": n_clicks},
#                                                 n_clicks=0,
# #                                                 style={"display": "block", 'margin-right': '10px'},
#                                             ))),
#                             dcc.Dropdown(
#                                                 options=drop_down_menu_list, 
#                                 placeholder="Select Table Name",
# #                                                 value = 'ap_case_safe', 
#                                                 id={"type": "table_dropdown", "index": n_clicks},
#                                             ),
#                             dcc.Dropdown(placeholder="Select Column Name",
#                                                 id={"type": "column_dropdown", "index": n_clicks},
#                                             ),
#                             dcc.Dropdown(placeholder="Select Match Type",
#                                                 options = ['Exactly Match', 'Contain'],
#                                                 id={"type": "radio_button_1", "index": n_clicks},
#                                             ),
#                             dcc.Dropdown(placeholder="Select Search Logic",
#                                                 options = ['AND', 'OR', 'NOT'],
#                                 value = 'OR',
#                                                 id={"type": "logic_choice", "index": n_clicks},
#                                             ),

#                             dbc.Input(
#                                         id={'type':'input_1', 'index': n_clicks,},
#                                         placeholder="Input keyword ...",
#                                         persistence=False,
#                                         autocomplete="off",
#                                     ),
#             ],
#         )
#         children.append(new_element)
#     return children

# @app.callback(
#     Output({"type": "column_dropdown", "index": MATCH}, "options"),
#     Input({"type": "table_dropdown", "index": MATCH}, "value"),
# )


# def update_column_dropdown(table_dropdown):
#     return list(data_dict[table_dropdown].columns)

# @app.callback(
#     Output({"type": "input_1", "index": MATCH}, 'list'),
#     Input({"type": "input_1", "index": MATCH}, "value"),
#     Input({"type": "table_dropdown", "index": MATCH}, "value"),
#     Input({"type": "column_dropdown", "index": MATCH}, "value"),
# )
# def suggest_locs(input_1, table_dropdown, column_dropdown):
#     return_string = 'datalist' + '_' + str(table_dropdown) + '_' + str(column_dropdown)
#     return return_string

# @app.callback(
#     Output("display_selected_values_2", "children"),
#     Input({"type": "table_dropdown", "index": ALL}, "value"),
#     Input({"type": "column_dropdown", "index": ALL}, "value"),
#     Input({"type": "input_1", "index": ALL}, "value"),
#     Input({"type": "radio_button_1", "index": ALL}, "value"),
#     Input({"type": "logic_choice", "index": ALL}, "value"),
#     Input({"type": "filter_badge", "index": ALL}, "children"),
# )


# def set_display_filters_info(table_dropdown, column_dropdown, 
#                              input_1, radio_button_1, logic_choice, filter_badge):
# #     print(filter_badge)
#     filter_badge_int_list = []
#     for one_badge in filter_badge:
#         filter_badge_int_list.append(int(one_badge[9:-2]))
# #     all_chain_list = {}
#     for n_clicks_index in range(len(table_dropdown)):
#         all_chain_list[str(filter_badge_int_list[n_clicks_index])] = [table_dropdown[n_clicks_index], 
#                                                column_dropdown[n_clicks_index], 
#                                                radio_button_1[n_clicks_index],
#                                                logic_choice[n_clicks_index],
#                                                input_1[n_clicks_index],
#                                               ]
# #     print(all_chain_list)
    
#     return_list = []
    
# #     return_list.append(dbc.Row(dbc.Col(html.Div('Filters info list'))))
    
# #     for one_key in list(all_chain_list.keys()):
#     for one_key in filter_badge_int_list:
#         one_key = str(one_key)
#         return_string = ''
#         return_string += "Filter "
#         return_string += str(one_key)
#         return_string += ': '
#         return_string += str(all_chain_list[one_key])
#         return_list.append(dbc.Row(dbc.Col(html.Div(return_string))))
        
#     return return_list

# @app.callback(
#     Output("logic_input", "value"),
#     Input("display_selected_values_2", "children"),
# )

# def display_logic_input(display_selected_values_2):
    
#     return_string = ''
    
#     if len(list(all_chain_list.keys())) == 1:
#         return_string = '(1)'
#         return return_string
        
#     if len(list(all_chain_list.keys())) == 2:
#         return_string = '(1 ' + str(all_chain_list['2'][3]) + ' 2)'
#         return return_string
    
#     key_count = 0
#     for one_key in list(all_chain_list.keys()):
#         if key_count == 0:
#             return_string = '(' + str(one_key) + ')'
#         if key_count == 1:
#             return_string = '(1 ' + str(all_chain_list['2'][3]) + ' 2)'
#         else:
#             return_string = '(' + return_string
#             return_string += ' '
#             return_string += str(all_chain_list[one_key][3])
#             return_string += ' '
#             return_string += str(one_key)
#             return_string += ')'
        
#         key_count += 1
#     return return_string

# @app.callback(
#     [Output("table", "data"),
#     Output("table", "columns"),],
#     Input("final-query", "n_clicks"),
#     Input('table', "page_current"),
#     Input('table', "page_size"),
#     Input('table', 'sort_by'),
#     Input('table', 'filter_query'),
#     Input('logic_input', 'value'),
#     State("final_input", "value"),
# )

# def display_table(n_clicks, 
#                   page_current, page_size, 
#                   sort_by, filter_query, logic_input,
#                   final_input):
#     if n_clicks is None:
#         raise PreventUpdate
#     else: 
#         all_filter_dict = all_chain_list
# #         print(all_filter_dict)
#         filter_number = int(list(all_filter_dict.keys())[-1])
#         add_number = 0
#         for one_letter in logic_input:
#             if one_letter == '(':
#                 add_number += 1

#         if ('AND' not in logic_input) and ('OR' not in logic_input) and ('NOT' not in logic_input):
            
#             one_filter_list = all_filter_dict[logic_input[1:-1]]
#             table_name = one_filter_list[0]
#             search_table = data_dict[table_name]
#             column_name = one_filter_list[1]
#             keyword = one_filter_list[4]
#             exact_or_not = one_filter_list[2]
            
#             if exact_or_not == 'Exactly Match':
#                 keyword = ' ' + keyword + ' '
#             else:
#                 keyword = keyword
            
#             final_index = list(search_table['id_safe'][search_table[column_name].str.lower().str.contains(keyword)])
            
#             final_output_data_list = []
#             for one_table in final_input:
#                 final_output_data_list.append(data_dict[one_table][data_dict[one_table]['id_safe'].isin(final_index)])

#             final_data = reduce(lambda  left,right: pd.merge(left,right,on=['id_safe'], how='outer'), final_output_data_list)
# #             final_data = final_data.head(100)
            
#         else:
            
#             total_loop_number = filter_number + add_number + 50
#             total_index_dict = {}
#             for one_number in range(total_loop_number, -1, -1):
#                 if str(one_number) in logic_input:
#                     one_filter_list = all_filter_dict[str(one_number)]
#                     table_name = one_filter_list[0]
#                     search_table = data_dict[table_name]
#                     column_name = one_filter_list[1]
#                     keyword = one_filter_list[4]
#                     exact_or_not = one_filter_list[2]
                    
#                     if exact_or_not == 'Exactly Match':
#                         keyword = ' ' + keyword + ' '
#                     else:
#                         keyword = keyword
                    
#                     index_list = list(search_table['id_safe'][search_table[column_name].str.lower().str.contains(keyword)])

#                     total_index_dict[str(one_number)] = index_list
#             possible_conbination_list = []
#             for first_number in range(total_loop_number):
#                 for second_number in range(total_loop_number):
#                     for logic_conditions in ['AND', 'OR', 'NOT']:
#                         possible_conbination_list.append(str(first_number) + ' ' + logic_conditions + ' ' + str(second_number))

#             possible_conbination_list = Sorting(possible_conbination_list)

#             conbination_index = 0
#             replace_index_number = filter_number + 1
#             while conbination_index < len(possible_conbination_list):
#                 conbination = possible_conbination_list[conbination_index]
#                 if conbination not in logic_input:
#                     conbination_index += 1
#                     continue
#                 else:
#                     start_position = logic_input.find(conbination)
#                     end_position = start_position + len(conbination)

#                     for one_number in range(total_loop_number, -1, -1):
#                         if str(one_number) in conbination:
#                             one_number_start_position = conbination.find(str(one_number))
#                             if one_number_start_position == 0:
#                                 first_list_index = one_number
#                             else:
#                                 second_list_index = one_number
#                         else:
#                             continue

#                     if 'AND' in conbination:
#                         total_index_dict[str(replace_index_number)] = list(set(total_index_dict[str(first_list_index)]).intersection(total_index_dict[str(second_list_index)]))
#                         replace_index_number += 1
#                     elif 'OR' in conbination:
#                         total_index_dict[str(replace_index_number)] = list(set(total_index_dict[str(first_list_index)] + total_index_dict[str(second_list_index)]))
#                         replace_index_number += 1
#                     elif 'NOT' in conbination:
#                         append_new_list = []
#                         for one_element in total_index_dict[str(first_list_index)]:
#                             if one_element in total_index_dict[str(second_list_index)]:
#                                 continue
#                             else:
#                                 append_new_list.append(one_element)
#                         total_index_dict[str(replace_index_number)] = list(set(append_new_list))
#                         replace_index_number += 1 

#                     logic_input = logic_input[:(start_position-1)] + str(replace_index_number - 1) + logic_input[(end_position + 1):]

#                     conbination_index = 0

#             final_index = total_index_dict[str(logic_input)]
#             final_output_data_list = []
#             for one_table in final_input:
#                 final_output_data_list.append(data_dict[one_table][data_dict[one_table]['id_safe'].isin(final_index)])

#             final_data = reduce(lambda  left,right: pd.merge(left,right,on=['id_safe'], how='outer'), final_output_data_list)
# #             final_data = final_data.head(100)
      
#         filtering_expressions = filter_query.split(' && ')
#         dff = final_data
#         for filter_part in filtering_expressions:
#             col_name, operator, filter_value = split_filter_part(filter_part)

#             if operator in ('eq', 'ne', 'lt', 'le', 'gt', 'ge'):
#                 dff = dff.loc[getattr(dff[col_name], operator)(filter_value)]
#             elif operator == 'contains':
#                 dff = dff.loc[dff[col_name].str.lower().str.contains(filter_value.lower())]
#             elif operator == 'datestartswith':
#                 dff = dff.loc[dff[col_name].str.startswith(filter_value)]

#         if len(sort_by):
#             dff = dff.sort_values(
#                 [col['column_id'] for col in sort_by],
#                 ascending=[
#                     col['direction'] == 'asc'
#                     for col in sort_by
#                 ],
#                 inplace=False
#             )

#         page = page_current
#         size = page_size
        
#         final_data_columns = [{"name": i, "id": i} for i in dff.columns]
#         return dff.iloc[page * size: (page + 1) * size].to_dict('records'), final_data_columns

# app.layout = html.Div([sidebar, maindiv])
    
# # app.run_server(debug=False,mode="external",host='localhost', port=8805)
# if __name__ == '__main__':
#     app.run_server(debug=False,
#         # mode="external",host='localhost', 
#         port=8850)

