from freediving_analysis import collect_data_aida


df = collect_data_aida.get_results_events(range(10,5000))

print(df)

df.to_csv('data/aida_competiton.csv')