"""CSC110 COVID-19 Final Project: Modelling the Canadian Housing Market

Copyright and Usage Information
===============================

This file is Copyright (c) 2021 Terence Liu, Woojin Jang, and Charlie Tao.
"""
import plotly.graph_objects as go
import datetime


# Create line graph traces
def graph_data(data: dict[str: dict[datetime: float]]) -> None:
    """Create a graph with plotly using the provided data. Can take in multiple line data to create
    multiple lines on one graph.
    """
    fig = go.Figure()
    colors = ['lime', 'gold', 'purple', 'orange', 'red', 'blue']

    for line in data:
        x_values = list(data[line].keys())
        y_values = list(data[line].values())

        fig.add_trace(go.Scatter(x=x_values, y=y_values,
                                 mode='lines',
                                 name=line,
                                 line=dict(color=colors.pop(), width=4)))

    # Label axis
    fig.update_layout(title='Predicted House Pricing',
                      xaxis_title='Year',
                      yaxis_title='Money (Thousand)')

    fig.show()
