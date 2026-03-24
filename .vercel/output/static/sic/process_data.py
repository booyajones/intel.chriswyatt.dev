import pandas as pd
import numpy as np
import json
import os

def compute_gini(array):
    array = array.flatten()
    if np.amin(array) < 0:
        array -= np.amin(array)
    array = np.sort(array)
    index = np.arange(1, array.shape[0] + 1)
    n = array.shape[0]
    return ((np.sum((2 * index - n - 1) * array)) / (n * np.sum(array)))

def get_lorenz_curve(array):
    array = np.sort(array.flatten())
    array = array[array > 0]
    n = array.shape[0]
    lorenz_y = np.cumsum(array) / np.sum(array)
    lorenz_y = np.insert(lorenz_y, 0, 0)
    lorenz_x = np.linspace(0.0, 1.0, lorenz_y.size)
    # Downsample to 100 points
    idx = np.linspace(0, len(lorenz_x)-1, 100).astype(int)
    return lorenz_x[idx].tolist(), lorenz_y[idx].tolist()

def main():
    print("Reading data...")
    df = pd.read_csv('../merged_analysis_data.csv')
    df['total_spend'] = pd.to_numeric(df['total_spend'], errors='coerce').fillna(0)
    df['total_payments'] = pd.to_numeric(df['total_payments'], errors='coerce').fillna(0)
    df = df[df['total_payments'] > 0]
    
    df['avg_ticket'] = df['total_spend'] / df['total_payments']
    df['freq'] = df['total_payments'] / 30.0
    
    # 1. Lorenz & Gini
    print("Computing Lorenz & Gini...")
    gini_spend = compute_gini(df['total_spend'].values)
    gini_freq = compute_gini(df['total_payments'].values)
    lx_spend, ly_spend = get_lorenz_curve(df['total_spend'].values)
    lx_freq, ly_freq = get_lorenz_curve(df['total_payments'].values)
    
    # 2. 2x2 Quadrant logic
    # split at medians (or fixed $2500 and 2.5/month per plan)
    print("Computing Quadrants...")
    med_ticket = 2500.0
    med_freq = 2.5
    
    df['quadrant'] = 'Unknown'
    q1 = (df['avg_ticket'] >= med_ticket) & (df['freq'] >= med_freq) # High T, High F
    q2 = (df['avg_ticket'] >= med_ticket) & (df['freq'] < med_freq)  # High T, Low F
    q3 = (df['avg_ticket'] < med_ticket) & (df['freq'] >= med_freq)  # Low T, High F
    q4 = (df['avg_ticket'] < med_ticket) & (df['freq'] < med_freq)   # Low T, Low F
    
    df.loc[q1, 'quadrant'] = 'Q1: Strategic Partners'
    df.loc[q2, 'quadrant'] = 'Q2: Capital Events'
    df.loc[q3, 'quadrant'] = 'Q3: Operational Noise'
    df.loc[q4, 'quadrant'] = 'Q4: Long Tail'
    
    # Downsample scatter plot data for rendering (e.g., 2000 random points)
    df_sample = df.sample(n=min(3000, len(df)), random_state=42)
    scatter_data = []
    for _, row in df_sample.iterrows():
        scatter_data.append({
            'x': round(row['avg_ticket'], 2),
            'y': round(row['freq'], 2),
            'quadrant': row['quadrant']
        })
        
    # 3. Decile breakdown
    print("Computing Deciles...")
    # Spend deciles
    df['spend_decile'] = pd.qcut(df['total_spend'], 10, labels=False, duplicates='drop') + 1
    decile_summary = df.groupby('spend_decile').agg({
        'total_spend': 'sum',
        'total_payments': 'sum',
        'avg_ticket': 'mean',
        'freq': 'mean',
        'sic_code': 'count'
    }).rename(columns={'sic_code': 'supplier_count'}).reset_index()
    
    decile_summary['avg_ticket'] = decile_summary['avg_ticket'].round(2)
    decile_summary['total_spend'] = decile_summary['total_spend'].round(2)
    decile_summary['freq'] = decile_summary['freq'].round(2)
    decile_summary_list = decile_summary.to_dict('records')
    
    # Quadrant Summary
    quad_summary = df.groupby('quadrant').agg({
        'total_spend': 'sum',
        'sic_code': 'count'
    }).rename(columns={'sic_code': 'supplier_count'}).reset_index()
    
    # Build JS object
    out_dict = {
        'gini': {
            'spend': round(gini_spend, 4),
            'frequency': round(gini_freq, 4)
        },
        'lorenz': {
            'x': lx_spend,
            'y_spend': ly_spend,
            'y_freq': ly_freq
        },
        'quadrants': {
            'medians': {'ticket': med_ticket, 'freq': med_freq},
            'summary': quad_summary.to_dict('records'),
            'scatter': scatter_data
        },
        'deciles': decile_summary_list
    }
    
    print("Writing JS...")
    js_code = f"var sicData = {json.dumps(out_dict, indent=2)};"
    with open('sic_data.js', 'w', encoding='utf-8') as f:
        f.write(js_code)
    print("Done.")

if __name__ == '__main__':
    main()
