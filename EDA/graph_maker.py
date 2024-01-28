import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go

"""
Generates plots to download for EDA because interactive plots do not show up in pdf-format
"""

#Create data
df_clinical = pd.read_csv('D:\HW\Radiomics\EDA_folder\OPC_clinical_old.csv')
df_ct = pd.read_csv('D:\HW\Radiomics\EDA_folder\OPC_radiomics_old.csv', header=1)

df_clinical['patient'] = pd.to_numeric(df_clinical['Trial PatientID'].str.replace('OPC-', '').str.lstrip('0'))
df_clinical.drop('Trial PatientID', axis=1, inplace=True)
merged = df_ct.merge(df_clinical, left_on='patient', right_on='patient') #replace df_ct with df_ct[columns]
merged.replace({',': '.'}, regex=True, inplace=True)


# create smoking_py.png
df = px.data.tips()
fig = px.violin(df_clinical, y="Smoking PY")
fig.update_layout(width=600,height=600)
fig.show()


# create status_volume.png and status_coarseness.png
for y_axis in ['original_shape_VoxelVolume', 'original_ngtdm_Coarseness']:
    fig = go.Figure()
    color = 'Sex'
    color_options = merged[color].unique()
    fig.add_trace(go.Violin(x=merged['Status'][merged[color] == color_options[0] ],
                            y=merged[y_axis][merged[color] == color_options[0] ],
                            legendgroup='Yes', scalegroup='Yes', name=color_options[0],
                            side='negative',
                            line_color='blue')
                )
    fig.add_trace(go.Violin(x=merged['Status'][merged[color] == color_options[1] ],
                            y=merged[y_axis][merged[color] == color_options[1] ],
                            legendgroup='No', scalegroup='No', name=color_options[1],
                            side='positive',
                            line_color='orange')
                )
    fig.update_traces(meanline_visible=True)
    fig.update_layout(title=f"Violin Plot ({'Status'} vs\n{y_axis})",
                            width=600,height=600)
    fig.show()


# create status_coarseness_scaled.png
fig = go.Figure()
color = 'Sex'
color_options = merged[color].unique()
fig.add_trace(go.Violin(x=merged['Status'][merged[color] == color_options[0] ],
                        y=merged['original_ngtdm_Coarseness'][merged[color] == color_options[0] ],
                        legendgroup='Yes', scalegroup='Yes', name=color_options[0],
                        side='negative',
                        line_color='blue')
            )
fig.add_trace(go.Violin(x=merged['Status'][merged[color] == color_options[1] ],
                        y=merged['original_ngtdm_Coarseness'][merged[color] == color_options[1] ],
                        legendgroup='No', scalegroup='No', name=color_options[1],
                        side='positive',
                        line_color='orange')
            )
fig.update_traces(meanline_visible=True)
fig.update_layout(title=f"Violin Plot ({'Status'} vs\n{'original_ngtdm_Coarseness'})",
                        width=600,height=600)
fig.update_layout(yaxis_range=[-0.0005,0.002])
fig.show()

# create chemo_age.png
fig = go.Figure()
color = 'Sex'
color_options = merged[color].unique()
merged['Age at diagnosis'] = [float(str(x).replace(',', '.')) for x in merged['Age at diagnosis']]
fig.add_trace(go.Violin(x=merged['Chemotherapy'][merged[color] == color_options[0] ],
                        y=merged['Age at diagnosis'][merged[color] == color_options[0] ],
                        legendgroup='Yes', scalegroup='Yes', name=color_options[0],
                        side='negative',
                        line_color='blue')
            )
fig.add_trace(go.Violin(x=merged['Chemotherapy'][merged[color] == color_options[1] ],
                        y=merged['Age at diagnosis'][merged[color] == color_options[1] ],
                        legendgroup='No', scalegroup='No', name=color_options[1],
                        side='positive',
                        line_color='orange')
            )
fig.update_traces(meanline_visible=True)
fig.update_layout(title=f"Violin Plot ({'Chemotherapy'} vs\n{'Age at diagnosis'})",
                        width=600,height=600)
fig.show()