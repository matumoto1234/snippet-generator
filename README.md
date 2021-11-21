# snippet-generator
vscode snippet-generator for library

## sunippet-generator とは
ライブラリからスニペットを自動で生成してくれるものです。  
より正確には指定されたパス以下のファイルを再帰的に探索し、json形式で`template.code-snippets.json`というファイルに出力します。  
フォーマットはされていないので、各自でフォーマットしたのちに自分のスニペットをコピペしてください。  
生成されるスニペットの `scope` の値は `cpp` 固定になっています。

## 必要な環境
- `pythonが使用できる`(必要なバージョンはわからない)
- `glob`, `yaml`, `json` などが import できる

## 使い方
`main.py` と同じディレクトリにある `config.yml` に `paths` を追記していきます。

例.  
```yaml
paths: 
  - '/home/matumoto/library/data-strucuture'
  - '/home/matumoto/library/graph'
  - '/home/matumoto/library/math'
```

`paths` には絶対パスを指定してください。  
`cpp` などのファイルの一つ上の階層を指定してください。  
ディレクトリが内部にあった場合の動作は未定義です。

## お問い合わせ
なにかバグを見つけた、もしくは修正してほしい機能などがあったらこのリポジトリへ Issue を投げてください。
