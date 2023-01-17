import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from sklearn.metrics import roc_curve, roc_auc_score, precision_recall_curve, recall_score, precision_score, accuracy_score

def plot_precision_recall_acc_curve(y_true, y_pred,dataset_name, width=None, height=None):
    thresholds = np.linspace(0, 1, 101) 
    accuracy = []
    precision = []
    recall = []
    for ths in thresholds:
        accuracy.append(accuracy_score(y_true, y_pred>ths))
        precision.append(precision_score(y_true, y_pred>ths))
        recall.append(recall_score(y_true, y_pred>ths))

    df = pd.DataFrame({'precision': precision[1:-1], 'recall': recall[1:-1], 'accuracy':accuracy[1:-1], 'threshold': thresholds[1:-1]})
    fig = go.Figure()
    fig.add_trace(go.Scatter( 
                            x=df['threshold'],y=df['accuracy'],
                            line=dict(color=px.colors.qualitative.Pastel[0], width=4),
                            mode='lines+markers',
                            name='accuracy'
                            )
                )
    fig.add_trace(go.Scatter(
                            x=df['threshold'], y=df['recall'],
                            line=dict(color=px.colors.qualitative.Pastel[1], width=4),
                            mode='lines+markers',
                            name='recall'
                            )
                )
    fig.add_trace(go.Scatter(   
                                x=df['threshold'], y=df['precision'],
                                line=dict(color=px.colors.qualitative.Pastel[2], width=4),
                                mode='lines+markers', name='precision'
                            )
                )
    fig.update_layout(
                        title= f'Threshold of confidence to scroe metrics - {dataset_name} set',
                        xaxis_title='Threshold of confidence',
                        legend_title='Metric'
                   )
    if width:
        fig.update_layout(width=width, height=height)
    fig.show()

def plot_pred_dist(y_true, y_pred, width=None, height=None):
    df = pd.DataFrame({'y_true': y_true, 'y_pred': y_pred})
    fig = go.Figure()
    fig.add_trace(go.Histogram(x=df['y_pred'].loc[df['y_true']==0],name='label = 0'))
    fig.add_trace(go.Histogram(x=df['y_pred'].loc[df['y_true']==1],name='label = 1'))

    # Overlay both histograms
    fig.update_layout(barmode='overlay',title="distrabution of prediction's confidacnt on the diffrernt labels")
    if width:
        fig.update_layout(width=width, height=height)
    # Reduce opacity to see both histograms
    fig.update_traces(opacity=0.75)
    fig.show()