import panel as pn
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pandas.api.types import is_numeric_dtype
from bokeh.plotting import figure
from bokeh.transform import factor_cmap
pn.extension('plotly')
pn.extension()

def read_data():
    #read the 2 dataframes
    df_clinical = pd.read_csv('OPC_data_clinical.csv')
    df_ct = pd.read_csv('OPC_CT_radiomics_TCIA.csv', header=1)
    
    #merge the 2 dataframes into new dataframe: merged
    df_clinical['patient'] = pd.to_numeric(df_clinical['Trial PatientID'].str.replace('OPC-', '').str.lstrip('0'))
    df_clinical.drop('Trial PatientID', axis=1, inplace=True)
    merged = df_ct.merge(df_clinical, left_on='patient', right_on='patient') #replace df_ct with df_ct[columns]
    merged.replace({',': '.'}, regex=True, inplace=True)
    for column in ['Age at diagnosis', 'Smoking PY', 'Dose (gy)']:
        merged[column] = [float(str(x).replace(',', '.')) for x in merged[column]]
    
    #print(merged['original_shape_Maximum3DD'])
    #open preference.csv, a file containing which column should be on top, and which should be left out/not shown.
    with open('preferences.csv', newline='') as f:
        file = list(f)
        preference = {'+':file[1].split(',')}
        preference['+'][-1] = preference['+'][-1].replace('\r\n','')
        if len(file) >3:
            preference['-'] = file[3].split(',')

    return df_clinical, df_ct, merged, preference

def create_asked_columns(df_clinical, df_ct, preference):
    """
    Creates 2 dictionaries

    """
    clinical_columns = {'rest':list(df_clinical.columns)}
    ct_columns = {'rest':list(df_ct.columns)}
    clinical_columns['pref'] = list()
    ct_columns['pref'] = list()

    for i in preference['+']:
        if i in clinical_columns['rest']:
            clinical_columns['rest'].remove(i)
            clinical_columns['pref'].append(i)
        elif i in ct_columns['rest']:
            ct_columns['rest'].remove(i)
            ct_columns['pref'].append(i)
    if len(preference.keys()) > 1:
        for i in preference['-']:
            if i in clinical_columns['rest']:
                clinical_columns['rest'].remove(i)
            elif i in ct_columns['rest']:
                ct_columns['rest'].remove(i)

    return clinical_columns, ct_columns

def dropdown(clinical_columns, ct_columns, data):
    """
    Creates a dropdown menu showing which option are recommended and which are probably less usefull.
    """
    return pn.widgets.Select(name='Selecteer een optie', groups={'Aangeraden klinische kolommen':clinical_columns['pref'], 'Overige klinische kolommen':clinical_columns['rest'],
                                                                 'Aangeraden CT kolommen':ct_columns['pref'], 'Overige CT kolommen':ct_columns['rest']})
    #return pn.widgets.Select(name='Selecteer een optie', options=list(data.columns))

def plot_chooser(x_col, y_col): #Choose between violin, bar and scatter
    """
    Looks at the choosen x and y axis and chooses the best graph type,
    calls the function corresponding to the choosen graph type.

    If both x and y are numeric it chooses scatterplot.
    If only 1 of the 2 axis is numeric, and the x-axis contains 8 or less unique values it choose violinplot.
    If only 1 of the 2 axis is numeric, and the x-axis contains 9 or more unique values it choose barplot,
    if both x and y are not numeric it also chooses barplot.
    """
    x_type = is_numeric_dtype(merged[x_col])
    y_type = is_numeric_dtype(merged[y_col])
    print(f'{merged[x_col].values[0]}, {merged[y_col].values[0]} - {x_type}, {y_type}')
    if x_type and y_type:
        return scatter_plot(x_col, y_col)
    elif not x_type and not y_type:
        return bar_plot(x_col, y_col)
    elif x_type != y_type:
        if len(merged[x_col].unique()) > 8:
            return bar_plot(x_col, y_col)
        else:
            return violin_plot(x_col, y_col)

def scatter_plot(x_col, y_col):
    color = factor_cmap('Status', palette=['orange', 'blue'], factors=['Dead', 'Alive'])

    p = figure(title=f"Scatter Plot ({x_col} vs\n{y_col})", width=550, height=550)
    p.xaxis.axis_label = x_col
    p.yaxis.axis_label = y_col
    
    p.scatter(x_col, y_col, color=color, source=merged, size=10, alpha=0.75, legend_field='Status')
    return p

def bar_plot(x_axis, y_axis):
    """
    info_status = merged.groupby(x_axis)[y_axis].value_counts().unstack()
    #percentile = df_ct.groupby(x_axis)[y_axis].quantile()
    ax = info_status.plot(kind='bar', rot=30, stacked=True)
    print('bar')
    return plt
    """
    if y_axis == 'Sex':
        barmode = 'stack'
    else:
        barmode = 'group'
    fig = px.bar(merged, x=x_axis, color=y_axis, barmode=barmode,
                 title=f"Bar Plot ({x_axis} vs\n{y_axis})", )
    fig.update_layout(autosize=False,width=600,height=600,)
    return fig

def violin_plot(x_axis, y_axis):
    """
    """
    fig = go.Figure()
    if x_axis == 'Status' or y_axis == 'Status':
        color = 'Sex'
    else:
        color = 'Status'
    color_options = merged[color].unique()

    fig.add_trace(go.Violin(x=merged[x_axis][merged[color] == color_options[0] ],
                            y=merged[y_axis][merged[color] == color_options[0] ],
                            legendgroup='Yes', scalegroup='Yes', name=color_options[0],
                            side='negative',
                            line_color='blue')
                )
    fig.add_trace(go.Violin(x=merged[x_axis][merged[color] == color_options[1] ],
                            y=merged[y_axis][merged[color] == color_options[1] ],
                            legendgroup='No', scalegroup='No', name=color_options[1],
                            side='positive',
                            line_color='orange')
                )
    fig.update_traces(meanline_visible=True)
    fig.update_layout(title=f"Violin Plot ({x_axis} vs\n{y_axis})",
                          width=600,height=600)
    return fig

if __name__ == "__main__":
    df_clinical, df_ct, merged, preference = read_data() #create dataframes
    clinical_columns, ct_columns = create_asked_columns(df_clinical, df_ct, preference)
    #scatter_layout = pn.interact(scatter_plot, x_col=dropdown(), y_col=dropdown())
    #scatter_layout2 = pn.interact(scatter_plot2, x_col=dropdown(df), y_col=dropdown(df))

    layout = pn.interact(plot_chooser, x_col=dropdown(clinical_columns, ct_columns, merged),
                                 y_col=dropdown(clinical_columns, ct_columns, merged))
    layout2 = pn.interact(plot_chooser, x_col=dropdown(clinical_columns, ct_columns, merged),
                                  y_col=dropdown(clinical_columns, ct_columns, merged))

    app = pn.template.BootstrapTemplate(title='Radiomics')
    app.sidebar.append(pn.Column('Plot 1',layout[0], 2*'\n','Plot 2', layout2[0]))
    
    app.main.append(pn.Row((pn.Column(
        pn.Row(align="center"),
        layout[1],)),'',(pn.Column( # '' creates space between graphs
        pn.Row(align="center"),
        layout2[1],))))
    
    app.show()
