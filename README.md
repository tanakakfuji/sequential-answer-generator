# sequential-answer-generator
対話スレッド単位で質問から回答を自動生成するツール（OpenAI・Ollamaに対応）

## クイックスタート
- 仮想環境の作成

```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

- [OpenAI Platform](https://platform.openai.com/api-keys) より、APIキーを作成・コピー

- `.env` ファイルを作成

```bash
cp .env.example .env
nano .env
```

- APIキーを設定

```bash
OPENAI_MODEL_NAME=gpt-5-nano
OPENAI_API_KEY=【作成したAPIキー】
OLLAMA_MODEL_NAME=

CONVERSATION_BUFFER_TURNS=2
REQUEST_INTERVAL_TIME=2.0
```

- 実行例

```bash
python -m src.main --client openai --prompt data/prompts/sample_prompt.txt --query data/queries/sample_query.csv --output_dir sample_dir
```

## ドキュメント

### 入力ファイルのデータ形式
`data/queries` 配下に、質問リストのcsvファイルを配置します。

ただし、以下の形式では、エラーが生じます。

- 必須のカラム名（conversation_idとquery）が存在しない
- conversation_idまたはqueryの値が空文字の行が存在する

また、csvファイル内で、conversation_idは連続していなくてもよいですが、conversation_idが同じ質問は、上から下に時系列に並べる必要があります。

### プロンプト
`data/prompts` 配下に、システムプロンプト用のテキストファイルを配置します。
ユーザープロンプトは、質問リストのqueryをそのまま用います。

### オプション
実行時に利用できるオプションは以下の通りです。

|オプション名|必要性|説明|
|--|--|--|
|--client {openai, ollama}|required|回答生成に使用するクライアントツールを指定|
|--prompt|required|システムプロンプトのテキストファイルを指定|
|--query|required|クエリのcsvファイルを指定|
|--output_dir|required|生成結果の出力先を指定|

### 環境変数
実行時に指定する環境変数は以下の通りです。

|変数名|説明|
|--|--|
|OPENAI_MODEL_NAME|OpenAIが提供するモデルの名前を指定|
|OPENAI_API_KEY|APIキーを指定|
|OLLAMA_MODEL_NAME|Ollamaが提供するモデルの名前を指定|
|REQUEST_INTERVAL_TIME|リクエストを送信する間隔を秒数で指定|
|CONVERSATION_BUFFER_TURNS|直近の対話履歴を保持するターン数を指定|

※ Difyのメモリ機能におけるウィンドウサイズは、直近の対話履歴とユーザープロンプトを合わせた値になる。よって、`CONVERSATION_BUFFER_TURNS={Difyのウィンドウサイズ} - 1` となる点に注意。

### 出力結果
`outputs/{output_dir}` 配下にresults.csvが出力されます。データ形式は以下の通りです。

- results.csv (answer列に生成結果が格納)

```
conversation_id, query, answer,status
aaaaaa,aaaaaa,aaaaaa,success
bbbbbb,bbbbbb,bbbbbb,success
cccccc,cccccc,cccccc,success
```

### テスト
`tests` 配下にテストファイルがあり、以下の通りテストを実行できます。

```bash
pytest --cov=src --cov-report=term-missing
```
