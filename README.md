# snippet-generator
vscode snippet-generator for library

## sunippet-generator とは
ライブラリからVSCode用のスニペットを自動で生成してくれるものです。  
`config.yml`により指定されたパス以下のファイルを再帰的に探索し、`template.code-snippets.json`というファイルに出力します。  

## 必要な環境
- `python3.8` 以上で正常な動作を確認しています

## 使い方
`config.yml` で以下の設定が可能です。

- paths: 文字列配列  
  `paths` には絶対パスもしくは実行時のディレクトリからの相対パスを指定してください。  
  指定したパス以下のファイルを再帰的に探索し、各ファイルのスニペットを作成します。

- prefix: 文字列
  snippet の `prefix` には拡張子を除いたファイル名が入りますが、それの接頭辞を指定できます。  
  `prefix: 'cpp'` と設定した場合は `cppsegment_tree` などになります。

- excludeLines: 文字列配列  
  `#pragma once` などの、スニペットから除外したい行を指定してください。  
  `hoge*` などの正規表現が扱え、マッチする行が除外されます。

- excludeExtensions: 文字列配列
  スニペット生成から除外したい拡張子を指定できます。

- prefixNameCase: 'Snake' | 'Pascal' | 'Kebab' | 'Camel'  | ''
  生成されるスニペットの呼び出し部分(prefix)の命名規則を指定できます。  
  'Snake', 'Pascal', 'Kebab', 'Camel' 以外を指定した場合はそのままのファイル名になります。
  例：`cppsegment_tree` や `cppsegment-tree`

- jsonIndent: 正整数
  生成するjsonのインデントを指定できます。

- useOjBundle: True | False
  `oj-bundle` をし、`#include "hoge.hpp"` などを展開したスニペットを生成するかを選べます。

- scope: 文字列
  snippetの`scope`にはいる部分を指定できます。


例として [sample.config.yml](https://github.com/matumoto1234/snippet-generator/blob/master/sample.config.yml) があります

## 注意点

- 読み込んだファイル名の命名規則はケバブケース想定で書いています。（TODO：直す）


## お問い合わせ
なにかバグを見つけた、もしくは修正してほしい機能などがあったらこのリポジトリへ Issue を投げるか Twitter の @matumoto_1234 へご連絡ください。
