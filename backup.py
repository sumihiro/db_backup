import argparse
import yaml
import os
import subprocess
from datetime import datetime, timedelta

def load_config(script_dir, quiet=False):
    config_path = os.path.join(script_dir, 'config.yaml')
    log_message(f"設定ファイル: {config_path}", quiet)
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

def create_backup_directory(base_dir, host, database):
    backup_dir = os.path.join(base_dir, 'backup', host, database)
    os.makedirs(backup_dir, exist_ok=True)
    return backup_dir

def log_message(message, quiet=False):
    if not quiet:
        print(message)

def backup_database(host, database, user, password, backup_dir, quiet=False):
    today = datetime.now().strftime('%Y-%m-%d')
    filename = f"{today}.sql"
    backup_path = os.path.join(backup_dir, filename)
    
    command = f"mysqldump -h {host} -u {user} -p{password} {database} > {backup_path}"
    subprocess.run(command, shell=True, check=True)
    log_message(f"バックアップを作成: {host} - {database}", quiet)

def remove_old_backups(backup_dir, retention_days, quiet=False):
    today = datetime.now().date()
    log_message(f"削除対象のバックアップディレクトリ: {backup_dir}", quiet)
    log_message(f"保持する日数: {retention_days}日", quiet)
    
    for file in os.listdir(backup_dir):
        if file.endswith('.sql'):
            file_path = os.path.join(backup_dir, file)
            try:
                file_date = datetime.strptime(file.split('.')[0], '%Y-%m-%d').date()
                age_days = (today - file_date).days
                log_message(f"ファイル: {file}, 作成日: {file_date}, 経過日数: {age_days}日", quiet)
                if age_days >= retention_days:
                    os.remove(file_path)
                    log_message(f"削除されたファイル: {file_path}", quiet)
            except ValueError:
                log_message(f"無効なファイル名形式: {file}", quiet)

def main():
    parser = argparse.ArgumentParser(description='データベースバックアップスクリプト')
    parser.add_argument('-q', '--quiet', action='store_true', help='出力を抑制します')
    args = parser.parse_args()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    config = load_config(script_dir, args.quiet)

    base_dir = config.get('output_directory', script_dir)
    
    for db in config['databases']:
        backup_dir = create_backup_directory(base_dir, db['host'], db['database'])
        backup_database(db['host'], db['database'], db['user'], db['password'], backup_dir, args.quiet)
        remove_old_backups(backup_dir, config['retention_days'], args.quiet)

if __name__ == "__main__":
    main()

