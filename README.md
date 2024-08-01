# データベースバックアップスクリプト

このプロジェクトは、複数のMySQLデータベースを定期的にバックアップするためのPythonスクリプトを提供します。

## 機能

- 複数のデータベースを指定してバックアップ
- バックアップファイルの保存期間の設定
- 古いバックアップファイルの自動削除
- カスタム出力ディレクトリの指定（オプション）
- クワイエットモードでの実行（出力抑制）

## 必要条件

- Python 3.6以上
- PyYAML
- MySQLクライアント（mysqldump）

## セットアップ

1. このリポジトリをクローンまたはダウンロードします。

2. 必要なPythonパッケージをインストールします：

   ```
   pip install pyyaml
   ```

3. `config.yaml.example`を`config.yaml`にコピーし、必要な情報を入力します。

## 設定

`config.yaml`ファイルで以下の設定が可能です：

- `retention_days`: バックアップファイルを保持する日数
- `output_directory`: バックアップファイルの保存先ディレクトリ（オプション）
  - 指定しない場合、スクリプトが存在するディレクトリ以下の`backup`ディレクトリが使用されます
- `databases`: バックアップ対象のデータベース情報（複数指定可能）

設定例：

  ```yaml
  retention_days: 14
  output_directory: "/path/to/custom/backup/directory"
  databases:
    - host: "127.0.0.1"
      database: "db1"
      user: "user1"
      password: "password1"
    - host: "remote_host"
      database: "db2"
      user: "user2"
      password: "password2"
    # 必要に応じて他のデータベースを追加
  ```

## 使用方法

1. `backup.py`スクリプトを実行します：

   通常モード（出力あり）：
   ```
   python backup.py
   ```

   クワイエットモード（出力なし）：
   ```
   python backup.py -q
   ```
   または
   ```
   python backup.py --quiet
   ```

2. バックアップファイルは`output_directory`で指定されたディレクトリ（未指定の場合は`backup/ホスト名/データベース名/`）に`YYYY-MM-DD.sql`の形式で保存されます。

3. 指定した保持期間を超えた古いバックアップファイルは自動的に削除されます。

## 定期実行の設定

cronを使用して毎日自動実行するには、以下のようなcron jobを設定します：

```
0 1 * * * /usr/bin/python /path/to/backup.py
```

これにより、毎日午前1時にバックアップスクリプトが実行されます。

## トラブルシューティング

スクリプトが正しく動作しない場合は、以下を確認してください：

1. `config.yaml`ファイルが正しく設定されているか
2. データベースの接続情報が正確か
3. 必要なパッケージがすべてインストールされているか
4. バックアップディレクトリに書き込み権限があるか

問題が解決しない場合は、スクリプトの出力ログを確認し、エラーメッセージを参照してください。

## `pip` が使えない環境での実行方法

レンタルサーバなど、root権限がない場合や `pip` が使用できない場合は、以下の手順で依存パッケージをインストールし、スクリプトを実行することが可能です。

1. ユーザーのホームディレクトリにPythonのライブラリを保存するディレクトリを作成します：

```
mkdir -p ~/python_libs
```

2. PyYAMLのソースコードをダウンロードします：

```
cd ~/python_libs
wget https://pypi.org/packages/source/P/PyYAML/PyYAML-6.0.tar.gz
tar -xzvf PyYAML-6.0.tar.gz
cd PyYAML-6.0
```

3. セットアップスクリプトを実行して、ユーザーのホームディレクトリにインストールします：

```
python3 setup.py install --user
```

4. PYTHONPATHを設定して、Pythonがこのライブラリを見つけられるようにします。~/.bashrcや~/.bash_profileに以下の行を追加します：

```
export PYTHONPATH=$HOME/.local/lib/python3.x/site-packages:$PYTHONPATH
```

（python3.xの部分は、使用しているPythonのバージョンに合わせて変更してください）

5. 設定を反映させるため、シェルを再起動するか、以下のコマンドを実行します：

```
source ~/.bashrc  # または ~/.bash_profile
```

さらに、cronを使用して実行する場合は、以下の方法を試してみてください：

1. `cron_backup.sh` を開き、それぞれのパスを使用している環境に合わせて修正します：

```
#!/bin/bash
export PYTHONPATH=$HOME/.local/lib/python3.x/site-packages:$PYTHONPATH
/usr/bin/python3 /path/to/your/backup.py
```

2. `crontab` ではこのシェルスクリプトを実行するように設定します：

```
0 1 * * * /path/to/cron_backup.sh
```


## ライセンス

このプロジェクトはMITライセンスの下で公開されています。詳細については、`LICENSE`ファイルを参照してください。
