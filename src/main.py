from src.utils import load_text, load_csv, save_csv
from src.generator import generate
import argparse
from collections import defaultdict

def main():
  parser = argparse.ArgumentParser(description='対話スレッド単位で質問から回答を自動生成するツール')
  parser.add_argument('--client', type=str, choices=['openai', 'ollama'], required=True, help='回答生成に使用するクライアントツールを指定')
  parser.add_argument('--prompt', type=str, required=True, help='システムプロンプトのテキストファイルを指定', metavar='data/prompts/sample_prompt.txt')
  parser.add_argument('--query', type=str, required=True, help='クエリのcsvファイルを指定', metavar='data/queries/sample_query.csv')
  parser.add_argument('--output_dir', type=str, required=True, help='生成結果の出力先を指定', metavar='sample_dir')
  args = parser.parse_args()

  system_prompt = load_text(args.prompt)
  query_data = load_csv(args.query)
  row_count = len(query_data) - 1
  queries_list = _build_data(query_data)
  outputs, error_count = generate(args.client, system_prompt, queries_list, row_count)
  save_csv(outputs, f'outputs/{args.output_dir}', 'results.csv')
  print(f'エラー件数: {error_count}')
  print(f'outputs/{args.output_dir} に生成結果を出力しました')

def _build_data(data):
  try:
    conv_idx, query_idx = data[0].index('conversation_id'), data[0].index('query')
  except ValueError as e:
    raise KeyError('csvファイルにはconversation_id、queryキーが必要です')
  categorized_data = defaultdict(list)
  for i in range(len(data)):
    if i == 0: continue
    if not data[i][conv_idx]:
      raise ValueError(f'{str(i)}行目のconversaion_idが空です')
    if not data[i][query_idx]:
      raise ValueError(f'{str(i)}行目のqueryが空です')
    categorized_data[data[i][conv_idx]].append({
      'conversation_id': data[i][conv_idx],
      'query': data[i][query_idx],
    })
  
  queries_list = list(categorized_data.values())
  return queries_list

if __name__ == '__main__':
  main()
