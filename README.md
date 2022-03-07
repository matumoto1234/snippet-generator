# snippet-generator
vscode snippet-generator for library

## sunippet-generator とは
ライブラリからスニペットを自動で生成してくれるものです。  
`config.yml`により指定されたパス以下のファイルを再帰的に探索し、`template.code-snippets.json`というファイルに出力します。  

## 必要な環境
- `pythonが使用できる`(必要なバージョンはわからない)
- `glob`, `yaml`, `json` などが import できる

## 使い方
`main.py` と同じディレクトリにある `config.yml` 以下の形式で設定を書きます。

- paths: 文字列配列
  `paths` には絶対パスを指定してください。  
  指定したパス以下を再帰的に探索し、スニペットを作成します。
- excludeLines: 文字列配列
  `#pragma once` などの、スニペットに含めたくない内容をしてください。
  指定したものが含まれている行がスニペットに表示されなくなります。
- prefixNameCase: 'Snake' | 'Pascal' | 'Kebab' | 'Camel'
  生成されるスニペットの呼び出し部分(prefix)の命名規則を指定できます。  
  例：`cppsegment_tree` や `cppsegment-tree`
- useOjBundle: True | False
  `oj-bundle` を行ったスニペットを生成するかを選べます。
  `#line` などは自動的に削除されます。


例.  
```yaml
paths: 
  - '/home/matumoto/library/data-strucuture'
  - '/home/matumoto/library/graph'
  - '/home/matumoto/library/math/mod-factorial.hpp'

excludeLines:
  - '#pragma once'

prefixNameCase: 'Snake'

useOjBundle: True
```

## 注意点

- 読み込んだファイル名の命名規則はケバブケース想定で書いています。（TODO：直す）
- スニペットの`prefix`には`cpp`の接頭辞がつきます（TODO：`config.yml`でいじれるよう修正する）
- スニペットの`scope`には`cpp`が自動的に指定されます。（TODO：`config.yml`でいじれるよう修正する）
- `config.yml`に一つでも設定を記述しなかったら未定義動作になります。（TODO：デフォルト値を設定しておく）



## お問い合わせ
なにかバグを見つけた、もしくは修正してほしい機能などがあったらこのリポジトリへ Issue を投げてください。
