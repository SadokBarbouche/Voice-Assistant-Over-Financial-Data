import pandas as pd
import json

input_file = 'data/sujet_dataset.csv'
output_file = 'data/fixed_sujet_dataset.csv'

def clean_and_parse_json(json_string):
    cleaned_string = json_string.replace('xx', '')
    return json.loads(cleaned_string)

if __name__ == "__main__":
    df = pd.read_csv(input_file)
    
    df['question'] = df['question'].apply(clean_and_parse_json)
    df['context'] = df['context'].apply(clean_and_parse_json)
    
    df.to_csv(output_file, index=False)
    print("'xx' removed and JSON parsed for 'question' and 'context'. Results saved to:", output_file)