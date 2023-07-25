import requests
import pandas as pd

class Wikidata:
    def __init__(self):
        pass

    def url_sparql_query(self, sparql_url: str, output_format: str = 'dict'):
        r = requests.get(sparql_url, headers={'accept': 'application/sparql-results+json'})
        if r.status_code != 200:
            return
        
        if output_format == "dataframe":
            return self.df_sparql_results(json_results=r.json())
        
        return r.json()

    def simplify_sparql_results(self, json_results: dict):
        if "results" not in json_results and "bindings" not in json_results["results"]:
            return

        data_records = []
        var_names = json_results['head']['vars']

        for record in json_results['results']['bindings']:
            data_record = {}
            for var_name in var_names:
                data_record[var_name] = record[var_name]['value'] if var_name in record else None
            data_records.append(data_record)
        
        return data_records

    def df_sparql_results(self, json_results: dict):
        data_records = self.simplify_sparql_results(json_results)
        return pd.DataFrame(data_records)
