import matplotlib.pyplot as plt
import pandas as pd

#Load data from both datasets.
def read_data():
    return pd.read_csv('Radiomics/OPC_data_clinical - Sheet1.csv')
df = read_data()
def read_data_ct():
    return pd.read_csv('Radiomics/OPC_CT_radiomics_TCIA - Sheet1.csv')
df_ct = read_data_ct()


def create_graph_drinking(df):
    """
    Creates a graph showing the influence of drinking on the survival change/rate.
    """
    x_axis = 'Drinking hx'
    y_axis = 'Status'

    info_status = df.groupby(x_axis)[y_axis].value_counts().unstack()
    #percentile = df_ct.groupby(x_axis)[y_axis].quantile()
    ax = info_status.plot(kind='bar', rot=30, stacked=True)
    plt.show()
create_graph_drinking(df)

def tumor_dimension(df, df_ct):
    """
    Generate graph for the physical dimensions of the tumor and if the patient survives.
    Usefull for seeing which aspects of the tumor are most dangerous.
    Merges the 2 dataframes into 1 new dataframe.
    """
    dimensions = ['patient', 'original_shape_Elongation','original_shape_Flatness','original_shape_LeastAxisLength',\
        'original_shape_MajorAxisLength','original_shape_Maximum2DDiameterColumn',\
            'original_shape_Maximum2DDiameterRow','original_shape_Maximum2DDiameterSlice',\
                'original_shape_Maximum3DDiameter','original_shape_MeshVolume',\
                    'original_shape_MinorAxisLength','original_shape_Sphericity','original_shape_SurfaceArea'\
                        ,'original_shape_SurfaceVolumeRatio','original_shape_VoxelVolume']
    dim = ['patient', 'original_shape_Elongation']
    ct = df_ct[dimensions]
    # status = df[['Trial PatientID','Status']]
    #ct['status'] = df['status']


    df['patient'] = pd.to_numeric(df['Trial PatientID'].str.replace('OPC-', '').str.lstrip('0'))
    df.drop('Trial PatientID', axis=1, inplace=True)
    status = df[['patient','Status','Sex']]
    result = ct.merge(status, left_on='patient', right_on='patient')

    mydict = dict()
    for i in dimensions:
        mydict[i] = result[i]
    print(mydict)

    info_status = result.groupby(dimensions)['Status'].value_counts() #values_count() moet waarschijnlijk weg
    ax = info_status.plot(kind='box', rot=30, stacked=False)
    #plt.xticks(range(15), dimensions, rotation = 45) 
    plt.show()

#tumor_dimension(df, df_ct)
