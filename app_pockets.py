
import ast, random, os, tempfile, time, sqlite3, urllib.request
import matplotlib, matplotlib.colors, matplotlib.pyplot as plt, seaborn as sns, pandas as pd, streamlit as st, streamlit_ext as ste, st_aggrid, py3Dmol, stmol

st.set_page_config(
    page_title='Expansion of the landscape of small-molecule binding sites by AlphaFold2',
    page_icon='🔬',
    layout='wide',
)

st.cache_resource.clear()

def uf(x):
    return '{:,}'.format(x)

def select_dataframe_row(df_, selected_row_index, height=400):
    gb = st_aggrid.GridOptionsBuilder.from_dataframe(df_)
    gb.configure_selection(selection_mode='single', use_checkbox=True, pre_selected_rows=[ selected_row_index ])
    gb.configure_grid_options(domLayout='normal')
    #gb.configure_pagination()
    #https://github.com/PablocFonseca/streamlit-aggrid/issues/57
    gb.configure_grid_options(onFirstDataRendered=st_aggrid.JsCode("""
    function(e) { 
        e.api.ensureIndexVisible(%d, 'middle');
    }
    """ % (selected_row_index,)).js_code)
    gridOptions = gb.build()
    gridResponse = st_aggrid.AgGrid(df_,
        gridOptions=gridOptions,
        #update_mode=st_aggrid.GridUpdateMode.SELECTION_CHANGED,
        fit_columns_on_grid_load=True,
        height=height,
        width='100%',
        enable_enterprise_modules=False,
        allow_unsafe_jscode=True,
    )
    if not(len(gridResponse['selected_rows']) > 0): time.sleep(5) # Prevent annoying row-not-selected errors during loading
    if len(gridResponse['selected_rows']) == 0: return None
    return gridResponse['selected_rows'][0]

@st.cache_resource
def read_af2_v3_(af2_id):
    url_ = f'https://alphafold.ebi.ac.uk/files/AF-{af2_id}-F1-model_v3.pdb'
    with urllib.request.urlopen(url_) as url:
        return url.read().decode('utf-8')

@st.cache_resource
def read_structures():
    return pd.read_csv('web_app_data/structures.tsv', sep='\t')

@st.cache_resource
def read_pockets():
    return pd.read_csv('web_app_data/pockets.tsv', sep='\t')

st.write(f'# Structures')
search_query = st.text_input(label='Search for gene name, Entrez or UniProt id:')
if (search_query == ''):
    structures_ = read_structures()
else:
    structures_ = read_structures()
    m_ = (structures_['gene_name'].str.contains(search_query)\
        | structures_['gene_id'].astype(str).str.contains(search_query)\
        | structures_['UniProtKB_ac'].str.contains(search_query)\
        ).fillna(False)
    structures_ = structures_.loc[m_]

sel_struct = select_dataframe_row(structures_.drop(['seq'], axis=1), selected_row_index=0, height=300)
sel_struct_af2_id = sel_struct['af2_id']
st.write(f'# Pockets for {sel_struct["UniProtKB_ac"]}')
sel_pocket = select_dataframe_row(read_pockets().query('struct_id == @sel_struct_af2_id'), selected_row_index=0, height=300)
st.write(sel_pocket)