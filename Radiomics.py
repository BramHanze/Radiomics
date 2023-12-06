import matplotlib.pyplot as plt
import pandas as pd

def read_data():
    return pd.read_csv('Radiomics/OPC_data_clinical - Sheet1.csv')
df = read_data()
def read_data_ct():
    return pd.read_csv('Radiomics/OPC_CT_radiomics_TCIA - Sheet1.csv')
df_ct = read_data_ct()


def create_graph_short(df):
    x_axis = 'Drinking hx'
    y_axis = 'Status'

    info_status = df.groupby(x_axis)[y_axis].value_counts().unstack()
    #percentile = df_ct.groupby(x_axis)[y_axis].quantile()
    ax = info_status.plot(kind='bar', rot=30, stacked=True)
    plt.show()
#create_graph_short(df)


def tumor_dimension(df, df_ct):
    dimensions = ['patient', 'original_shape_Elongation','original_shape_Flatness','original_shape_LeastAxisLength',\
        'original_shape_MajorAxisLength','original_shape_Maximum2DDiameterColumn',\
            'original_shape_Maximum2DDiameterRow','original_shape_Maximum2DDiameterSlice',\
                'original_shape_Maximum3DDiameter','original_shape_MeshVolume',\
                    'original_shape_MinorAxisLength','original_shape_Sphericity','original_shape_SurfaceArea'\
                        ,'original_shape_SurfaceVolumeRatio','original_shape_VoxelVolume']
    ct = df_ct[dimensions]
    # status = df[['Trial PatientID','Status']]
    #ct['status'] = df['status']

    #PatientIDs = list(status['Trial PatientID'])
    
    df['patient'] = pd.to_numeric(df['Trial PatientID'].str.replace('OPC-', '').str.lstrip('0'))
    df.drop('Trial PatientID', axis=1, inplace=True)
    status = df[['patient','Status','Sex']]
    result = ct.merge(status, left_on='patient', right_on='patient')

    info_status = result.groupby('Status')['Sex'].value_counts().unstack()
    ax = info_status.plot(kind='bar', rot=30, stacked=True)
    #plt.xticks(range(15), dimensions, rotation = 45) 
    plt.show()


tumor_dimension(df, df_ct)
